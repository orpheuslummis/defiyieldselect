# in case the app runs forever, we only keep the latest hour of information to avoid overflow
# using utc datetimes

from peewee import (CharField, Database, DateTimeField, FloatField, Model,
                    SqliteDatabase)
from dfo.config import DATA_PATH

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
