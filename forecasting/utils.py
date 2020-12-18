import pandas as pd
import matplotlib.pyplot as plt
import datautil


def get_pairs():
    """How many and which pairs do we have?"""
    return set(pd.read_csv(datautil.datas["bowhead_prices"])['Pair'])


def print_orcadefi_data(asset, pair, kind):
    #FIXME
    asset = asset.capitalize()
    pair = pair.upper()
    kind = kind.capitalize()

    filename = f"{asset}_{pair}_{kind}.csv"
    path = f"{PATH_DATA_ORCADEFI}/{filename}"
    data = pd.read_csv(path)
    print(data.head())


def plot_timeseries():
    ts_apr = datautil.get_ts_apr()
    print(ts_apr)
    ts_price = datautil.get_ts_price()
    print(ts_price)