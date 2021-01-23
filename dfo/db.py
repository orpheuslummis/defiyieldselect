import time
from datetime import datetime, timedelta, timezone

from peewee import (CharField, Database, DateTimeField, FloatField, Model,
                    SqliteDatabase, fn)

from dfo.config import DATA_PATH, MODEL_MAIN, PAST_HORIZON

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
    modelid = CharField()
    score = FloatField()
    class Meta:
        indexes = (
            (('token', 'datetime', 'modelid'), True),
        )


def prepared_db() -> Database:
    with database:
        database.create_tables([APR, Price, Result])
        return database


def latest_results() -> dict:
    """return latest group of results ordered by score"""
    with database:
        latest_time = Result.select(fn.Max(Result.datetime)).scalar()
        if latest_time == None:
            return {"error": "results are not yet ready"}
        q_results = Result.select().where(
            Result.datetime == latest_time,
            Result.modelid == MODEL_MAIN
        ).order_by(Result.score.desc()).dicts()
        results = {
            'scores': {},
            'last_update': latest_time,
            }
        for result in q_results:
            results['scores'][result['token']] = result['score']
        # TODO meta information such as modelid, model parameters, ...
        return results


def fresh_only() -> None:
    """
    periodically removing old entries
    in case the app runs forever, to avoid overflow
    """
    while True:
        time.sleep(PAST_HORIZON)
        stale = datetime.now(timezone.utc) - timedelta(seconds=PAST_HORIZON * 2)
        database = prepared_db()
        with database:
            n_apr = APR.delete().where(APR.datetime < stale).execute()
            n_price = Price.delete().where(Price.datetime < stale).execute()
            n_result = Result.delete().where(Result.datetime < stale).execute()
            print(f'cleared database entries older than {stale}. APR {n_apr}, Price {n_price}, Result {n_result} cleared')
