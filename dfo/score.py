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


def model_a(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """
    approach: multiply APR by a weighted slope of linear regression of price
    """
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope * PRICE_WEIGHT)
    apr_mean = data_apr['value'].mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_a: {token_apr} {price_factor=} * {apr_mean=} = {score=}")
    # price_stddev = data_price.std().value
    # apr_stddev = data_apr.std().value
    # print(f'{price_stddev=}')
    # print(f'{apr_stddev=}')
    return score


def model_b(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """
    approach: multiply APR by the cubed slope of linear regression of price
    """
    reg_price = linregress(data_price.seconds_since, data_price.value)
    price_factor = (1 + reg_price.slope)**3
    apr_mean = data_apr['value'].mean()
    score = price_factor * apr_mean
    if DEBUG: print(f"model_b: {token_apr} {price_factor=} * {apr_mean=} = {score=}")
    return score


def get_recent_dataframe_token(modelname: str, token_apr: str, now: datetime) -> Optional[pd.DataFrame]:
    """
    Return recent data of selected model
    
    Recentness is parameterized by PAST_HORIZON
    Normalizing sampling rate to SAMPLING_INTERVAL
    We assume the APR values are normalized in an APR (in practice each platform has a diffferent APR definition and we don't normalize that here). We divide by their mantissa to get a percentage rate.
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
        data = data.drop(columns=['id'])
        return data
    if modelname == 'APR':
        token = token_apr
        data = get_data(APR, token)
        # to percentage
        data.value = data.value.div(ORCA_API_MANTISSA)
    elif modelname == 'price':
        token = APR_TOKEN_TO_UNISWAPV2_TOKENS[token_apr]
        data = get_data(Price, token)
        # normalize for comparable slopes
        data.value = data.value/data.value.mean()
    else:
        raise Exception
    if len(data) == 0:
        return None
    # resample
    data.datetime = pd.to_datetime(data.datetime)
    data = data.set_index('datetime')
    data  = data.resample(SAMPLING_INTERVAL).mean().bfill()
    # obtain time relative to beginning of frame for regression
    data = data.reset_index()
    data.datetime = pd.to_numeric(data.datetime)
    data['seconds_since'] = (data.datetime - data.datetime[0])/int(1e9)
    # print(f'{modelname=}, {token=}')
    # print(f'{data}')
    return data


def dataframe_common_length(dfa: pd.DataFrame, dfb: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    min_length = min(dfa.shape[0], dfb.shape[0])
    dfa = dfa[-min_length:]
    dfb = dfb[-min_length:]
    assert dfa.shape == dfb.shape
    return (dfa, dfb)


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
        for token_apr in APR_TOKENS:
            data_apr = get_recent_dataframe_token('APR', token_apr, now)
            data_price = get_recent_dataframe_token('price', token_apr, now)
            if data_apr is None or data_price is None or len(data_apr) > 2 or len(data_price) >2:
                if DEBUG: print(f'scoring: skipping {token_apr} because we don\'t have enough recent data')
            else:
                data_price, data_apr = dataframe_common_length(data_price, data_apr)
                print(f'{data_apr=}')
                print(f'{data_price=}')
                # for model in models:
                #     token_score = model(token_apr, data_price, data_apr)
                #     store_result(datetime=now, token=token_apr, modelid=model.__name__, score=token_score)
