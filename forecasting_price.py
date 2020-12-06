import itertools
import os
import shelve
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
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
RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR+"/images", exist_ok=True)


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
    # memoization
    try:
        with shelve.open('data/processed_data') as db:
            timeseries_pairs = db['timeseries_pairs']
        # print("obtained data from DB")
    except KeyError:
        timeseries_pairs = preprocess_data(load_data_raw())
        with shelve.open('data/processed_data') as db:
            db['timeseries_pairs'] = timeseries_pairs
    
    forecasters = {
        "naive": NaiveForecaster,
        "poly": PolynomialTrendForecaster
        # ExponentialSmoothing,
        # AutoETS,
        # AutoARIMA,
        # ThetaForecaster,
    }

    regressors = [
        sklearn.linear_model.LinearRegression(),
        sklearn.linear_model.LogisticRegression(),
    ]

    forecaster_configs = {
        "naive": [
            {"strategy": "last"},
            {"strategy": "mean"},
            {"strategy": "drift"},
            # try out this 
            # try out that
        ],
        "poly": [
            {"degree": 1},
            {"degree": 2},
            {"degree": 3},
            # try ths out 
            # thy asd;lfjkasd;lfkj a;sdlkfj 
        ]
    }

    results = {}
    for forecaster_name in forecasters:
        forecaster_combinations = itertools.product(timeseries_pairs, regressors, forecaster_configs[forecaster_name])
        for p in forecaster_combinations:
            print(forecaster_name, *p)
            pair = p[0]
            regressor = p[1]
            regressor_name = regressor.__class__.__name__
            forecaster_config = p[2]
            forecaster = forecasters[forecaster_name](regressor, **forecaster_config)
            timeseries = timeseries_pairs[pair]
            results[f"{pair}_{regressor_name}_{forecaster_name}"] = None

            x_train, x_test = temporal_train_test_split(timeseries)
            forecaster.fit(x_train)
            fh = np.arange(len(x_test)) + 1  # FIXME robust?
            x_pred = forecaster.predict(fh)

            if os.getenv("YIELDS_PLOT") == "True":
                plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
                plt.title(f"{pair} with forecaster {forecaster_name}")
                plt.savefig(f"{RESULTS_DIR}/images/{pair}_{forecaster_name}_{datetime.now().isoformat()}.png")

            smape_loss_result = smape_loss(x_test, x_pred)
            print(f"{pair} {forecaster_namer} {regressor_namer} loss: {smape_loss_resultr}")
            results[f"{pair}_{regressor_name}_{forecaster_name}"] = smape_loss_result

        pd.DataFrame.from_dict(results).to_json(f"{RESULTS_DIR}/results_{datetime.now().isoformat()}.json", indent=4)
