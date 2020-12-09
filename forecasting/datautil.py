import pandas as pd

import config


datas = {
    "bowhead_prices": "data/bowhead_csvs/PairPrices4DEC.csv"
}


def load_data_raw(data_name):
    data = pd.read_csv(datas[data_name], parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def preprocess_data(data): # TODO make more general than just for specificially for bowhead_prices
    timeseries_pairs = {}
    for pair in data:
        timeseries = data[pair]
        # simpler pair name
        pair = pair.replace('/','_')
        # resampling to have constant sampling rate for broad compatibility
        timeseries_pairs[pair] = timeseries.resample(config.BIN_PERIOD).bfill()
    return timeseries_pairs