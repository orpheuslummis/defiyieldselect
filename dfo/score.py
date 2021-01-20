"""
take recent data
score: combine APR and price slope
submit results to db
"""

import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd
from scipy.stats import linregress

from dfo.config import (APR_TOKEN_TO_UNISWAPV2_TOKENS, DEBUG, INTERVAL,
                        PAST_HORIZON, SAMPLING_INTERVAL)
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
    past_time_lower_bound = datetime.now(timezone.utc) - timedelta(seconds=PAST_HORIZON)
    data = pd.DataFrame(list(model.select().where(
        model.datetime >= past_time_lower_bound,
        model.token == token
    ).dicts())) # TODO more efficient way than -> dict -> list -> dataframe
    if len(data) == 0:
        return None
    data = data.drop(columns=['id'])
    # resampling
    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.set_index('datetime')
    data  = data.resample(SAMPLING_INTERVAL).mean().bfill()
    # we use nanosecond timestamp
    data = data.reset_index()
    data['datetime'] = pd.to_numeric(data['datetime'])
    return data


def linreg(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame):
    """
    input:
    output:
    """
    token_price = APR_TOKEN_TO_UNISWAPV2_TOKENS[token_apr]
    
    # take the 'common denominator' of data length, to have the same size of most recent data
    min_length = min(data_apr.shape[0], data_price.shape[0])
    data_apr = data_apr[-min_length:]
    data_price = data_price[-min_length:]
    assert data_apr.shape == data_price.shape

    reg_apr = linregress(data_apr['datetime'], data_apr['value'])
    reg_price = linregress(data_price['datetime'], data_price['value'])
    return reg_apr, reg_price


def score(token_apr: str, data_price: pd.DataFrame, data_apr: pd.DataFrame) -> float:
    """
    we score every token_apr

    scoring: 

    linear regression of apr
    linear regression of price
    combine them to create a score

    interval_start, interval_end, regression_apr, regression_price, stddev, modelid
    """
    reg_apr, reg_price = linreg(token_apr, data_price, data_apr)
    score = reg_price.slope * reg_apr.slope
    if DEBUG: print(f'{token_apr} {reg_price.slope} * {reg_apr.slope=} = {score=}')
    return score


def store_result(token: str, score: float, datetime: datetime) -> None:
    with database:
        print(f'{token=}, {score=}, {datetime=}')
        Result.create(datetime=datetime, token=token, score=score)


def run() -> None:
    while True:
        now = datetime.now(timezone.utc)
        for token_apr in APR_TOKEN_TO_UNISWAPV2_TOKENS:
            data_apr = get_recent_dataframe_token('APR', token_apr)
            data_price = get_recent_dataframe_token('price', token_apr)
            if data_apr is None or data_price is None:
                print(f'scoring: skipping {token_apr} because for now we don\'t have recent data')
            else:
                results = score(token_apr, data_price, data_apr)
                store_result(token_apr, results, t_start)
        duration = (datetime.datetime.now() - t_start).total_seconds()
        if DEBUG: print(f'{duration=}')
        time.sleep(INTERVAL - duration)
