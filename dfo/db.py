import time

import datetime
from peewee import (CharField, Database, DateTimeField, FloatField, Model,
                    SqliteDatabase, fn)

from dfo.config import DATA_PATH, PAST_HORIZON

database = SqliteDatabase(f'{DATA_PATH}/dfo.db', pragmas={'journal_mode': 'wal'}) 


class BaseModel(Model):
    class Meta:
        database = database


class APR(BaseModel):
    datetime = DateTimeField()
    platform = CharField()
    token = CharField()
    value = FloatField()
    class Meta:
        indexes = (
            (('platform', 'token', 'datetime'), True),
        )


class Price(BaseModel):
    datetime = DateTimeField()
    token = CharField()
    value = FloatField()
    timesource = CharField(default='web3') # otherwise 'heuristic'
    class Meta:
        indexes = (
            (('token', 'datetime'), True),
        )


class Result(BaseModel):
    datetime = DateTimeField()
    token = CharField()
    score = FloatField()


def prepared_db() -> Database:
    with database:
        database.create_tables([APR, Price, Result])
        return database


def latest_scores() -> dict:
    with database:
        latest_time = Result.select(fn.Max(Result.datetime)).scalar()
        q_results = Result.select().where(Result.datetime == latest_time).order_by(Result.score.desc()).dicts()
        results = {
            'datetime': latest_time,
        }
        for result in q_results:
            results[result['token']] = result['score']
        return results


def fresh_only() -> None:
    """
    periodically removing old entries
    in case the app runs forever, to avoid overflow
    """
    while True:
        stale = datetime.datetime.utcnow() - datetime.timedelta(seconds=PAST_HORIZON * 2)
        database = prepared_db()
        with database:
            n_apr = APR.delete().where(APR.datetime < stale).execute()
            n_price = Price.delete().where(Price.datetime < stale).execute()
            n_result = Result.delete().where(Result.datetime < stale).execute()
            print(f'cleared database entries older than {stale}. APR {n_apr}, Price {n_price}, Result {n_result} ')
        time.sleep(PAST_HORIZON)