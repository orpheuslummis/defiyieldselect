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
# from sktime.forecasting.arima import AutoARIMA
from sklearn.neighbors import KNeighborsRegressor
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.ets import AutoETS
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series

import forecasters

warnings.simplefilter(action='ignore', category=FutureWarning)

PATH_DATA_PRICES = 'data/bowhead_csvs/PairPrices4DEC.csv'
BIN_PERIOD = '1h'
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')
TIME_FORMAT = '%Y-%m-%d_%H_%MZ'


forecasters = {
    "naive": NaiveForecaster,
    "poly": PolynomialTrendForecaster,
    "exponential": ExponentialSmoothing,
    "theta": ThetaForecaster,
    # "autoets": AutoETS,
    "reducedregression": ReducedRegressionForecaster,
    # "autoarima": AutoARIMA,
}

forecaster_configs = {
    "naive": {
        "last": {"strategy": "last"},
        "mean": {"strategy": "mean"},
        "drift": {"strategy": "drift"},
    },
    "poly": {
        "degree1_linear": {"degree": 1, "regressor": sklearn.linear_model.LinearRegression()},
        "degree1_forest": {"degree": 1, "regressor": RandomForestRegressor()},
        "degree1_ridge": {"degree": 1, "regressor": sklearn.linear_model.Ridge()},
        "degree2_linear": {"degree": 2, "regressor": sklearn.linear_model.LinearRegression()},
        "degree2_forest": {"degree": 2, "regressor": RandomForestRegressor()},
        "degree2_ridge": {"degree": 2, "regressor": sklearn.linear_model.Ridge()},
        "degree2_ridge_alpha05": {"degree": 2, "regressor": sklearn.linear_model.Ridge(alpha=0.5)},
        "degree2_ridge_alpha025": {"degree": 2, "regressor": sklearn.linear_model.Ridge(alpha=0.25)},
        "degree3_linear": {"degree": 3, "regressor": sklearn.linear_model.LinearRegression()},
        "degree3_forest": {"degree": 3, "regressor": RandomForestRegressor()},
    },
    "exponential": {
        "default": {},
        # "damped": {"damped": True},
        "trend_add": {"trend": "add"},
        "trend_mul": {"trend": "mul"},
        "remove_bias": {"remove_bias": True},
        "sp60": {"sp": 60},
    },
    "theta": {
        "default": {},
        "sp80": {"sp": 80},
        "sp100": {"sp": 100},
        "sp40": {"sp": 40},
        "sp60": {"sp": 60},
        "smooth05": {"smoothing_level": 0.5},
        "smooth1": {"smoothing_level": 1},
        "smooth2": {"smoothing_level": 2},
    },
    # "autoets": {
    #     "default": {},
    # },
    # "autoarima": {
    #     "default": {},
    # }
    "reducedregression": {
        "forest": {"regressor": RandomForestRegressor()},
        "forest_wl20": {"regressor": RandomForestRegressor(), "window_length": 20},
        "forest_wl30": {"regressor": RandomForestRegressor(), "window_length": 30},
        "forest_wl100": {"regressor": RandomForestRegressor(), "window_length": 100},
        "kneighbors1": {"regressor": KNeighborsRegressor(n_neighbors=1)},
        "kneighbors2": {"regressor": KNeighborsRegressor(n_neighbors=2)},
        "kneighbors3": {"regressor": KNeighborsRegressor(n_neighbors=3)},
        "kneighbors4": {"regressor": KNeighborsRegressor(n_neighbors=4)},
        "kneighbors5": {"regressor": KNeighborsRegressor(n_neighbors=5)},
    }
}


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


if __name__ == "__main__":
    try: # memoization
        with shelve.open('data/processed_data') as db:
            timeseries_pairs = db['timeseries_pairs']
    except Exception as e:
        timeseries_pairs = preprocess_data(load_data_raw())
        with shelve.open('data/processed_data') as db:
            db['timeseries_pairs'] = timeseries_pairs
    
    results = {pair: {} for pair in timeseries_pairs}
    results_path = f"{RESULTS_DIR}/results_{datetime.utcnow().strftime(TIME_FORMAT)}"
    os.makedirs(results_path, exist_ok=True)

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
            results[pair][f"{forecaster_name}_{forecaster_config_name}"] = smape_loss_result    

            if os.getenv("PLOTS") == "True":
                plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
                plt.title(f"{pair} {forecaster_name} {forecaster_config_name}")
                plt.savefig(f"{results_path}/{pair}_{forecaster_name}_{forecaster_config_name}_{datetime.utcnow().strftime(TIME_FORMAT)}.png")
                plt.close()

    pd.DataFrame.from_dict(results).to_json(f"{results_path}/result.json", indent=4)