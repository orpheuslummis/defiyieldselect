import itertools

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

PATH_DATA = 'data/PairPrices4DEC.csv'


def load_data():
    data = pd.read_csv(PATH_DATA, parse_dates=['Time'])
    timeseries_pairs = {}
    for pair in set(data['Pair']):
        df = data.query(f"Pair == '{pair}'")
        timeseries = pd.Series(list(df['Price']), index=df['Time'])
        timeseries_pairs[pair] = timeseries
    return timeseries_pairs


def prediction(timeseries, forecaster):
    x_train, x_test = temporal_train_test_split(timeseries)
    forecaster.fit(x_train)
    fh = 10 # FIXME
    x_pred = forecaster.predict(fh)
    print(pair, smape_loss(x_test, x_pred))


if __name__ == "__main__":
    timeseries_pairs = load_data()

    # displaying the plots is slow~
    for timeseries in timeseries_pairs:
        print(timeseries)
        plot_series(timeseries_pairs[timeseries])
        plt.show()

    regressors = [
        RandomForestRegressor(),
    ]

    forecasters = [
        ReducedRegressionForecaster,
    ]

    regressor_forecaster_pairs = itertools.product(regressors, forecasters)
    possibilities = itertools.product(regressor_forecaster_pairs, timeseries_pairs)
    for p in possibilities:
        # print(p)
        regressor = p[0][0]
        forecaster = p[0][1]
        timeseries = timeseries_pairs[p[1]]
        forecaster = forecaster(regressor)
        prediction(timeseries, forecaster)
