import pandas as pd
import shelve

import config

DATA_PATH = 'data'


datas = {
    "bowhead_prices": f"{DATA_PATH}/bowhead_csvs/PairPrices4DEC.csv",
    "bowhead_lend": f"{DATA_PATH}/bowhead_csvs/Lend4DEC.csv" 
}


def load_data_raw(data_name):
    data = pd.read_csv(datas[data_name], parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def load_data_memoized(data_name):
    # TODO include a preprocessor callback, then memoized the result of loading+preprocessing
    dbpath = f'{DATA_PATH}/preprocessed_datas.db'
    try:
        with shelve.open(dbpath) as db:
            data = db[data_name]
    except Exception as e:
        raw_data = load_data_raw(data_name)
        data = preprocess_data(raw_data)
        with shelve.open(dbpath) as db:
            db[data_name] = data
    return data


def preprocess_data(data): # TODO make more general than just for specificially for bowhead_prices
    timeseries_pairs = {}
    for pair in data:
        timeseries = data[pair]
        # simpler pair name
        pair = pair.replace('/','_')
        # resampling to have constant sampling rate for broad compatibility
        timeseries_pairs[pair] = timeseries.resample(config.BIN_PERIOD).bfill()
    return timeseries_pairs


def load_lend_data(): # dict of Series
    data_raw = pd.read_csv(datas["bowhead_lend"], parse_dates=['Time'])
    tokens = ['DUSDC', 'DSAI', 'DETH','DDAI']
    data = {}
    for t in tokens:
        data[t] = pd.Series(list(data_raw[f'{t}.1']), index=data_raw['Time'])
    return data