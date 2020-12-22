# from the bowhead csv files to nice csvs

import pandas as pd
import os

from config import *

data_files = {
    "bowhead_price": f"{DATA_PATH}/bowhead_historical/price.csv",
    "bowhead_apr": f"{DATA_PATH}/bowhead_historical/lend.csv" 
}

matchings = {
    'USDC_ETH': 'DUSDC',
    'DAI_ETH': 'DDAI',
}


def ts_price_loader(data):
    timeseries = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        ts = pd.Series(list(df['Price']), index=df['Time'])
        pair = pair.replace('/','_')
        timeseries[pair] = ts
        # timeseries[pair] = ts.resample(TIMESTEP_PERIOD).bfill()
    return timeseries


def ts_apr_loader(data):
    timeseries = {}
    tokens = ['DUSDC', 'DETH','DDAI']
    for name in tokens:
        ts = pd.Series(list(data[f'{name}.1']), index=data['Time'])
        timeseries[name] = ts
        # timeseries[name] = ts.resample(config.TIMESTEP_PERIOD).bfill()
    return timeseries


if __name__ == "__main__":
    df_price = pd.read_csv(data_files['bowhead_price'], parse_dates=['Time'])
    data_price = ts_price_loader(df_price)

    df_apr = pd.read_csv(data_files['bowhead_apr'], parse_dates=['Time'])
    data_apr = ts_apr_loader(df_apr)

    # include correspondences between pairs
    for m in matchings:
        data_price[matchings[m]] = data_price[m]

    # find the intersection of pairs in price and apr
    common_pairs = [pair for pair in list(data_apr.keys()) if pair in list(data_price.keys())]

    # create one DataFrame csv per pair, a multivariate timeseries
    os.makedirs(f'{DATA_PATH}/bowhead/', exist_ok=True)
    for pair in common_pairs:
        df = pd.concat([data_apr[pair], data_price[pair]], axis=1)
        df = df.rename(columns={0: 'apr', 1: 'price'})
        # df = df.resample(TIMESTEP_PERIOD).bfill()
        print(pair, df)
        df.to_csv(f'{DATA_PATH}/bowhead/{pair}.csv')
        # FIXME NaNs

        # print(f'{pair} apr\n{data_apr[pair]}')
        # print(f'{pair} price\n{data_price[pair]}')
        # data_apr[pair].to_csv(f'{DATA_PATH}/bowhead/{pair}_apr.csv') # FIXME platform
        # data_price[pair].to_csv(f'{DATA_PATH}/bowhead/{pair}_price.csv')