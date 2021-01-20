"""
take recent data
score: combine APR and price slope
submit results to db
"""

import datetime
import time
from typing import Optional, Set

import pandas as pd
from peewee import fn
from scipy.stats import linregress

from dfo.config import (APR_TOKEN_TO_UNISWAPV2_TOKENS, INTERVAL, PAST_HORIZON,
                        SAMPLING_INTERVAL)
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
    past_time_lower_bound = datetime.datetime.utcnow() - datetime.timedelta(seconds=PAST_HORIZON)
    data = pd.DataFrame(list(model.select().where(
        model.datetime >= past_time_lower_bound,
        model.token == token
    ).dicts())) # TODO more efficient way than -> dict -> list -> dataframe
    if len(data) == 0:
        return None
    # print(f'{modelname} {token} {data=}')
    data = data.drop(columns=['id'])
    # resampling
    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.set_index('datetime')
    data  = data.resample(SAMPLING_INTERVAL).mean().bfill()
    # we use nanosecond timestamp
    data = data.reset_index()
    data['datetime'] = pd.to_numeric(data['datetime'])
    return data


def get_apr_tokens() -> Set[str]:
    return set(pd.DataFrame(list(APR.select().dicts()))['token'])


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
    print(f'{token_apr} {reg_price.slope} * {reg_apr.slope=} = {score=}')
    return score


def store_result(token: str, score: float, now=datetime.datetime) -> None:
    with database:
        Result.create(datetime=now, token=token, score=score)


def display_scores() -> None:
    with database:
        latest_time = Result.select(fn.Max(Result.datetime)).scalar()
        q = Result.select().where(Result.datetime == latest_time).order_by(Result.score.desc()).dicts()
        if len(q) > 0:
            [print(f"{r['token']} score: {r['score']}") for r in q]


def run() -> None:
    while True:
        t_start = datetime.datetime.now()
        for token_apr in get_apr_tokens():
            data_apr = get_recent_dataframe_token('APR', token_apr)
            data_price = get_recent_dataframe_token('price', token_apr)
            if data_apr is None or data_price is None:
                print(f'scoring: skipping {token_apr} because for now we don\'t have recent data')
            else:
                results = score(token_apr, data_price, data_apr)
                store_result(token_apr, results, t_start)
        display_scores()
        duration = (datetime.datetime.now() - t_start).total_seconds()
        print(f'{duration=}')
        time.sleep(INTERVAL - duration)