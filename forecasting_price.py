import itertools
import os
import shelve
import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
# from sklearn.ensemble import RandomForestRegressor # TODO
# from sktime.forecasting.arima import AutoARIMA # TODO
# from sktime.forecasting.compose import ReducedRegressionForecaster # TODO
# from sktime.forecasting.ets import AutoETS # TODO
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
TIME_FORMAT = '%Y-%m-%d_%H_%MZ'


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
    try: # memoization
        with shelve.open('data/processed_data') as db:
            timeseries_pairs = db['timeseries_pairs']
    except KeyError:
        timeseries_pairs = preprocess_data(load_data_raw())
        with shelve.open('data/processed_data') as db:
            db['timeseries_pairs'] = timeseries_pairs
    
    forecasters = {
        "naive": NaiveForecaster,
        "poly": PolynomialTrendForecaster,
        "exponential": ExponentialSmoothing,
        "theta": ThetaForecaster,
        # AutoETS,
        # AutoARIMA,
    }

    forecaster_configs = {
        "naive": {
            "last": {"strategy": "last"},
            "mean": {"strategy": "mean"},
            "drift": {"strategy": "drift"},
        },
        "poly": {
            "degree1_linear": {"degree": 1, "regressor": sklearn.linear_model.LinearRegression()},
            # {"degree": 1, "regressor": sklearn.linear_model.LogisticRegression()},
            "degree2_linear": {"degree": 2, "regressor": sklearn.linear_model.LinearRegression()},
            # {"degree": 2, "regressor": sklearn.linear_model.LogisticRegression()},
            "degree3_linear": {"degree": 3, "regressor": sklearn.linear_model.LinearRegression()},
            # {"degree": 3, "regressor": sklearn.linear_model.LogisticRegression()},
        },
        "exponential": {
            "default": {},
        },
        "theta": {
            "default": {},
        },
    }

    results = {pair: {} for pair in timeseries_pairs}
    results_path = f"{RESULTS_DIR}/results_{datetime.utcnow().strftime(TIME_FORMAT)}"
    os.makedirs(results_path)

    for forecaster_name in forecasters:
        forecaster_combinations = itertools.product(timeseries_pairs, forecaster_configs[forecaster_name])
        for p in forecaster_combinations:
            print(forecaster_name, *p)
            pair = p[0]
            forecaster_config = forecaster_configs[forecaster_name][p[1]]
            forecaster_config_name = p[1]
            forecaster = forecasters[forecaster_name](**forecaster_config)
            timeseries = timeseries_pairs[pair]

            x_train, x_test = temporal_train_test_split(timeseries)
            forecaster.fit(x_train)
            fh = np.arange(len(x_test)) + 1  # FIXME robust?
            x_pred = forecaster.predict(fh)


            smape_loss_result = smape_loss(x_test, x_pred)
            try:
                results[pair][forecaster_name][forecaster_config_name] = smape_loss_result
            except KeyError as e:
                results[pair][forecaster_name] = {}
                results[pair][forecaster_name][forecaster_config_name] = smape_loss_result

            if os.getenv("YIELDS_PLOT") == "True":
                plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
                plt.title(f"{pair} {forecaster_name} {forecaster_config_name}")
                plt.savefig(f"{results_path}/{pair}_{forecaster_name}_{forecaster_config_name}_{datetime.utcnow().strftime(TIME_FORMAT)}.png")
    

    pd.DataFrame.from_dict(results).to_json(f"{results_path}/result.json", indent=4)
