"""
take recent data
score: combine APR and price slope
submit results to db
"""

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


def get_recent_dataframe_token(modelname: str, token_apr: str) -> Optional[pd.DataFrame]:
    """
    return recent data of selected model
    normalizing sampling rate to SAMPLING_INTERVAL
    recentness is parameterized by PAST_HORIZON
    a dataframe might have a different number of measurements than its complementary
    """
    if modelname == 'APR':
        model = APR
        token = token_apr
    elif modelname == 'price':
        model = Price
        token = APR_TOKEN_TO_UNISWAPV2_TOKENS[token_apr]
    else:
        raise Exception
    # obtain from db
    past_time_lower_bound = datetime.now(timezone.utc) - timedelta(seconds=PAST_HORIZON)
    data = pd.DataFrame(list(model.select().where(
        model.datetime >= past_time_lower_bound,
        model.token == token
    ).dicts())) # there probably is a more efficient way than -> dict -> list -> dataframe
    if len(data) == 0:
        return None
    data = data.drop(columns=['id'])
    # resampling
    data.datetime = pd.to_datetime(data.datetime)
    data = data.set_index('datetime')
    data  = data.resample(SAMPLING_INTERVAL).mean().bfill()
    # obtaining time relative to beginning of frame for regression
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


def model_a(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """
    approach: multiply APR by a weighted slope of linear regression of price
    """
    data_price, data_apr = dataframe_common_length(data_price, data_apr)
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope * PRICE_WEIGHT)
    apr_mean = data_apr['value'].div(ORCA_API_MANTISSA).mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_a: {token_apr} {price_factor=} * {apr_mean=} = {score=}")
    return score


def model_b(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """
    approach: multiply APR by the cubed slope of linear regression of price
    """
    data_price, data_apr = dataframe_common_length(data_price, data_apr)
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope)**3
    apr_mean = data_apr['value'].div(ORCA_API_MANTISSA).mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_b: {token_apr} {price_factor=} * {apr_mean=} = {score=}")
    return score


def store_result(datetime: datetime, token: str, modelid: str, score: float) -> None:
    with database:
        try:
            Result.create(datetime=datetime, token=token, modelid=modelid, score=score)
        except IntegrityError as e:
            print(f'store_result: ({datetime=} {token=} {modelid=} {score=}) - {e}')


def run() -> None:
    models = [
        model_a,
        model_b
    ]
    while True:
        time.sleep(INTERVAL)
        now = datetime.now(timezone.utc)
        for token_apr in APR_TOKENS:
            data_apr = get_recent_dataframe_token('APR', token_apr)
            data_price = get_recent_dataframe_token('price', token_apr)
            if data_apr is None or data_price is None or len(data_apr) < 2 or len(data_price) < 2:
                print(f'scoring: skipping {token_apr} because we don\'t have enough recent data')
            else:
                for model in models:
                    token_score = model(token_apr, data_price, data_apr)
                    store_result(datetime=now, token=token_apr, modelid=model.__name__, score=token_score)
