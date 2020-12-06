import itertools
import os
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.ets import AutoETS
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series

warnings.simplefilter(action='ignore', category=FutureWarning)

PATH_DATA_PRICES = 'data/csv/PairPrices4DEC.csv'
PATH_DATA_ORCADEFI = 'data/data_orcadefi'
PLATFORMS = ['aave', 'compound', 'dydx', 'fulcrum']
BIN_PERIOD = '1h'


def load_data_raw():
    data = pd.read_csv(PATH_DATA_PRICES, parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def preprocess_data(data):
    timeseries_pairs = {}
    for pair in data:
        timeseries = data[pair]
        # simpler pair name
        pair = pair.replace('/','_')
        # resampling to have constant sampling rate for broad compatibility
        timeseries_pairs[pair] = timeseries.resample(BIN_PERIOD).bfill()
    return timeseries_pairs


def display_plots(timeseries_pairs):
    for timeseries in timeseries_pairs:
        plot_series(timeseries_pairs[timeseries], list=[timeseries])
        plt.show()


if __name__ == "__main__":
    timeseries_pairs = preprocess_data(load_data_raw())
    # display_plots(timeseries_pairs)
    # [print(timeseries_pairs[t]) for t in timeseries_pairs]

    forecasters = {
        "poly1": PolynomialTrendForecaster(),
        "poly2": PolynomialTrendForecaster(degree=2),
        # "poly3": PolynomialTrendForecaster(degree=3),
        # "poly4": PolynomialTrendForecaster(degree=4),
        # "poly5": PolynomialTrendForecaster(degree=5),
        # "expsmoothing": ExponentialSmoothing(),
        # "autoets": AutoETS(),
        # "autoarima": AutoARIMA(),
        # "theta": ThetaForecaster(),
    }

    results = {pair: {} for pair in timeseries_pairs}

    possibilities = itertools.product(forecasters, timeseries_pairs)
    for p in possibilities:
        forecaster_name = p[0]
        forecaster = forecasters[forecaster_name]
        pair = p[1]
        timeseries = timeseries_pairs[pair]

        x_train, x_test = temporal_train_test_split(timeseries)
        forecaster.fit(x_train)
        fh = np.arange(len(x_test)) + 1  # FIXME robust?
        x_pred = forecaster.predict(fh)

        if os.getenv("YIELDS_PLOT") == "True":
            plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
            plt.title(f"{pair} with forecaster {forecaster_name}")
            plt.savefig(f"results/{pair}_{forecaster_name}_{datetime.now().isoformat()}.png")

        smape_loss_result = smape_loss(x_test, x_pred)
        print(f"{pair=} {forecaster_name=} {smape_loss_result=}")
        results[pair][forecaster_name] = smape_loss_result

    pd.DataFrame.from_dict(results).to_json(f"results/results_{datetime.now().isoformat()}.json", indent=4)

    for pair in timeseries_pairs:
        results_pair = results[pair]
        print(f"best forecaster with {pair}: {min(results_pair, key=results_pair.get)}")
