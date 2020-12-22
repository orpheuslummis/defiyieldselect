import pandas as pd
import shelve
from pathlib import Path

from sktime.forecasting.model_selection import temporal_train_test_split

from config import *


def pairs():
    ls = sorted(Path(f'{DATA_PATH}/bowhead/').glob('*.csv'))
    return set([f.stem.split('_')[0] for f in ls])


def get_pair_data_train(pair: str) -> pd.DataFrame:
    data = get_pair_data(pair)
    data_train, data_test = temporal_train_test_split(data, train_size=0.8)
    return data_train


def get_pair_data_test(pair: str) -> pd.DataFrame:
    data = get_pair_data(pair)
    data_train, data_test = temporal_train_test_split(data, train_size=0.8)
    return data_test


def get_pair_data(pair: str) -> pd.DataFrame:
    path = f'{DATA_PATH}/bowhead/{pair}.csv'
    datacsv = pd.read_csv(path, parse_dates=['Time'], index_col=['Time'])
    for feature in datacsv.columns:
        datacsv[feature] = datacsv[feature].fillna(method='bfill')
    datacsv = datacsv.resample(TIMESTEP_PERIOD).mean()
    data = datacsv
    return data


# def last_time_feature(feature: pd.Series) -> Timestamp:
#     return None


def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    ... #TODO


def horizon_of_pair(data: pd.DataFrame) -> int:
    """the shortest length of the columns"""
    lengths = []
    for i, col in enumerate(data.columns):
        lengths[i] = len(data[col])
    return min(lengths)