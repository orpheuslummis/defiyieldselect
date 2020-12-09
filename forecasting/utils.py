import pandas as pd
import matplotib.pyplot as plt


def get_pairs():
    """How many and which pairs do we have?"""
    return set(pd.read_csv(datas["bowhead_prices"])['Pair'])


def print_orcadefi_data(asset, pair, kind):
    """Just to have an idea of the scope"""
    asset = asset.capitalize()
    pair = pair.upper()
    kind = kind.capitalize()

    filename = f"{asset}_{pair}_{kind}.csv"
    path = f"{PATH_DATA_ORCADEFI}/{filename}"
    data = pd.read_csv(path)
    print(data.head())


def load_data():
    """Generate series for crypto pairs"""
    data = pd.read_csv(datas["bowhead_prices"], parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def load_data_traces():
    data = pd.read_csv(datas["bowhead_prices"], parse_dates=['Time'])
    time_series_pairs = {}

    for pair in set(data['Pair']):
        time_series_traces = traces.TimeSeries()
        df = data.query(f"Pair == '{pair}'")

        for sr in zip(df['Time'], df['Price']):
            # probably another format for time ?
            time_series_traces[sr[0].to_pydatetime()] = sr[1]

        time_series_pairs[pair] = time_series_traces

    return time_series_pairs


def load_data_raw():
    data = pd.read_csv(datas["bowhead_prices"], parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs



def display_data_plots():
    data = load_data_raw()