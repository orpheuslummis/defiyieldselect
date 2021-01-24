import random
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
from peewee import IntegrityError
from scipy.stats import linregress

from dfo.config import (APR_TOKEN_TO_UNISWAPV2_TOKENS, APR_TOKENS, DEBUG,
                        INTERVAL, ORCA_API_MANTISSA, PAST_HORIZON,
                        PRICE_WEIGHT, SAMPLING_INTERVAL)
from dfo.db import APR, Price, Result, prepared_db

database = prepared_db()


def model_a(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """approach: multiply APR by a weighted slope of linear regression of price"""
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope * PRICE_WEIGHT)
    apr_mean = data_apr['value'].mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_a: {score=:.3f} ({price_factor=:.3f} * {apr_mean=:.3f}) {token_apr}")
    return score


def model_b(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """approach: multiply APR by the cubed slope of linear regression of price"""
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope * PRICE_WEIGHT)**3
    apr_mean = data_apr['value'].mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_b: {score=:.3f} ({price_factor=:.3f} * {apr_mean=:.3f}) {token_apr}")
    return score


def model_c(*args) -> float:
    """approach: random baseline"""
    return random.random()


def get_recent_dataframe_token(modelname: str, token_apr: str, now: datetime) -> Optional[pd.DataFrame]:
    """
    Return recent data of selected model
    
    Recentness is parameterized by PAST_HORIZON
    Normalizing sampling rate to SAMPLING_INTERVAL
    We assume the APR values are normalized as APR (but in practice, each platform has a different APR definition and we don't normalize that here).
    We divide by their mantissa to get a percentage rate.
    We normalize the price values by diviving them by their mean

    Complementary dataframe (APR for Price, Price for APR) won't necessarily have the same number of measurements
    """
    # obtain data
    def get_data(model, token: str) -> pd.DataFrame:
        # there probably is a more efficient way than -> dict -> list -> dataframe
        data = pd.DataFrame(list(model.select().where(
            model.token == token,
            model.datetime >= now - timedelta(seconds=PAST_HORIZON),
        ).dicts()))
        return data
    if modelname == 'APR':
        token = token_apr
        data = get_data(APR, token)
        if len(data) == 0:
            return None
        # to percentage
        data.value = data.value.div(ORCA_API_MANTISSA)
    elif modelname == 'price':
        token = APR_TOKEN_TO_UNISWAPV2_TOKENS[token_apr]
        data = get_data(Price, token)
        if len(data) == 0:
            return None
        # normalize for comparable slopes
        data.value = data.value/data.value.mean()
    else:
        raise Exception
    # resample
    data.datetime = pd.to_datetime(data.datetime)
    data = data.set_index('datetime')
    data  = data.resample(SAMPLING_INTERVAL).mean().bfill()
    # obtain time relative to beginning of frame for regression
    data = data.reset_index()
    data.datetime = pd.to_numeric(data.datetime)
    data['seconds_since'] = (data.datetime - data.datetime[0])/int(1e9)
    return data


def dataframe_common_length(dfa: pd.DataFrame, dfb: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    min_length = min(dfa.shape[0], dfb.shape[0])
    dfa = dfa[-min_length:]
    dfb = dfb[-min_length:]
    assert dfa.shape == dfb.shape
    return (dfa, dfb)


def volatility_tie_breaker(scores: dict, volatilities: dict) -> dict:
    """
    if multiple scores are the same, we adjust them slightly prefering lower standard deviation
    we assume we've run this function on every new score before
    return the adjusted scores
    (functional but naive implementation)
    """
    INFINITESIMAL = 0.00000000000000001
    # find duplicate scores
    duplicate_scores = []
    for token in scores:
        scores_without_token = scores.copy()
        del(scores_without_token[token])
        if scores[token] in scores_without_token.values():
            duplicate_scores.append(token)
    # score them by volatility
    if len(duplicate_scores) > 1:
        duplicate_scores_by_volatility = sorted(duplicate_scores, key=lambda token: volatilities[token])
        new_scores = scores.copy()
        for i, token in enumerate(duplicate_scores_by_volatility):
            new_scores[token] = new_scores[token] + i*INFINITESIMAL
        return new_scores
    else:
        return scores


def store_result(datetime: datetime, token: str, modelid: str, score: float) -> None:
    with database:
        try:
            Result.create(datetime=datetime, token=token, modelid=modelid, score=score)
        except IntegrityError as e:
            print(f'store_result: ({datetime=} {token=} {modelid=} {score=}) - {e}')


def run() -> None:
    models = [
        model_a,
        model_b,
    ]
    while True:
        time.sleep(INTERVAL)
        now = datetime.now(timezone.utc)
        scores = {}
        volatilities = {}
        for token_apr in APR_TOKENS:
            data_apr = get_recent_dataframe_token('APR', token_apr, now)
            data_price = get_recent_dataframe_token('price', token_apr, now)
            if data_apr is None or data_price is None or len(data_apr) <= 2 or len(data_price) <= 2:
                if DEBUG: print(f'scoring: skipping {token_apr} because we don\'t have enough recent data')
                continue
            else:
                data_price, data_apr = dataframe_common_length(data_price, data_apr)
                volatilities[token_apr] = data_apr.std().value
                for model in models:
                    scores[token_apr] = model(token_apr, data_price, data_apr)
                    scores = volatility_tie_breaker(scores, volatilities)
                    store_result(datetime=now, token=token_apr, modelid=model.__name__, score=scores[token_apr])
