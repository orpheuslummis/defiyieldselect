import pandas as pd
import shelve

from sktime.benchmarking.base import BaseDataset

from config import *


data_files = {
    "bowhead_price": f"{DATA_PATH}/bowhead_historical/price.csv",
    "bowhead_apr": f"{DATA_PATH}/bowhead_historical/lend.csv" 
}


def memoized_processing(name, data, processor):
    dbpath = f'{DATA_PATH}/preprocessed_datas.db'
    try:
        with shelve.open(dbpath) as db:
            processed_data = db[name]
    except Exception as e:
        processed_data = processor(data)
        with shelve.open(dbpath) as db:
            db[name] = processed_data
    return processed_data


def get_ts_price():
    def ts_price_loader(data):
        timeseries = {}
        for pair in set(data['Pair']):
            df = data.query(f"Pair == '{pair}'")
            curve = pd.Series(list(df['Price']), index=df['Time'])
            pair = pair.replace('/','_')
            timeseries[pair] = curve.resample(config.BIN_PERIOD).bfill()
        return timeseries
    name = 'bowhead_price'
    data = pd.read_csv(data_files[name], parse_dates=['Time'])
    return memoized_processing(name, data, ts_price_loader)


def get_ts_apr():
    # for now just dydx
    def ts_apr_loader(data):
        timeseries = {}
        tokens = ['DUSDC', 'DETH','DDAI']
        for name in tokens:
            ts = pd.Series(list(data[f'{name}.1']), index=data['Time'])
            timeseries[name] = ts.resample(config.BIN_PERIOD).bfill()
        return timeseries
    name = 'bowhead_apr'
    data = pd.read_csv(data_files[name], parse_dates=['Time'])
    return memoized_processing(name, data, ts_apr_loader)



class BowheadDataset(BaseDataset):
    pass # TODO
    # ideally this is the common representation for the bowhead stuff
    # what is the benchmarking code expecting as DataFrame? 


class BowheadLiveDataset(BaseDataset):
    pass # TODO
    # what we will obtain from the API


class BowheadHistoricalDataset(BaseDataset):
    pass # TODO
    # data/bowhead/{price,lend}.csv
    # and they have different formats...



# load pair data for forecasting and tuning
# data['train']
# data['test']