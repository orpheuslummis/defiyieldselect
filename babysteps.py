import itertools

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series
import traces
import warnings
from datetime import datetime
warnings.simplefilter(action='ignore', category=FutureWarning)

PATH_DATA_PREDICTION = 'data/csv/PairPrices4DEC.csv'
PATH_DATA_ORCADEFI = 'data/data_orcadefi'
# YOURS:
# PATH_DATA_PREDICTION = 'data/PairPrices4DEC.csv'
platforms = ['aave', 'compound', 'dydx', 'fulcrum']

# I just wanna leave here for me:
# https://www.sktime.org/en/latest/examples/01_forecasting.html


def get_pairs():
    """How many and which pairs do we have?"""
    return set(pd.read_csv(PATH_DATA_PREDICTION)['Pair'])


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
    data = pd.read_csv(PATH_DATA_PREDICTION, parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def load_data_traces():
    data = pd.read_csv(PATH_DATA_PREDICTION, parse_dates=['Time'])
    time_series_pairs = {}

    for pair in set(data['Pair']):
        time_series_traces = traces.TimeSeries()
        df = data.query(f"Pair == '{pair}'")

        for sr in zip(df['Time'], df['Price']):
            # probably another format for time ?
            time_series_traces[sr[0].to_pydatetime()] = sr[1]

        time_series_pairs[pair] = time_series_traces

    return time_series_pairs


def prediction(timeseries, forecaster):
    x_train, x_test = temporal_train_test_split(timeseries)
    forecaster.fit(x_train)
    fh = 10 # FIXME
    x_pred = forecaster.predict(fh)
    print(smape_loss(x_test, x_pred))


def display_plots(timeseries_pairs):
    """Displaying plots"""
    # displaying the plots is slow~
    for timeseries in timeseries_pairs:
        print(timeseries)
        plot_series(timeseries_pairs[timeseries])
        plt.show()


def posibilities(timeseries_pairs):
    """hmm"""

    regressors = [
        RandomForestRegressor(),
    ]

    forecasters = [
        ReducedRegressionForecaster,
    ]

    regressor_forecaster_pairs = itertools.product(regressors, forecasters)
    possibilities = itertools.product(regressor_forecaster_pairs, timeseries_pairs)

    for p in possibilities:
        print(p)
        regressor = p[0][0]
        forecaster = p[0][1]
        timeseries = timeseries_pairs[p[1]]
        forecaster = forecaster(regressor)

        # do you mind?
        # prediction(timeseries, forecaster)

        # preroces
        preproces_timeseries(timeseries)

        # I think is easier to read like this. Specially for a dump like me
        x_train, x_test = temporal_train_test_split(timeseries)
        forecaster.fit(x_train)
        fh = np.array([10])  # FIXME
        x_pred = forecaster.predict(fh)
        print(smape_loss(x_test, x_pred))


def preproces_timeseries(timeserie):
    n = len(timeserie)

    start = timeserie[0][0]
    flag = start
    end = timeserie[n-1][0]
    seconds = (start - end).total_seconds()
    step = datetime.timedelta(seconds = int(seconds/n))

    while flag < end:
        print(flag.strftime('%Y-%m-%d %H:%M:%S'))
        flag += step


if __name__ == "__main__":
    # timeseries_pairs = load_data()

    timeseries_pairs = load_data_traces()
    # obj_iter = iter(timeseries_pairs)
    # print(timeseries_pairs[next(obj_iter)].)

    # print_orcadefi_data(asset="aave", pair="abat", kind="borrow")
    # print(get_pairs())
    posibilities(timeseries_pairs)
    # series_preprocesing(timeseries_pairs)

