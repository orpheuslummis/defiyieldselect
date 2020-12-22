from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sktime.forecasting.compose import (EnsembleForecaster,
                                        ReducedRegressionForecaster)
from sktime.regression.compose import TimeSeriesForestRegressor

F1 = EnsembleForecaster([
        ('rr_linear_wl7', ReducedRegressionForecaster(LinearRegression(), window_length=7)),
        # ('rr_linear_wl21', ReducedRegressionForecaster(LinearRegression(), window_length=21)),
        # ('rr_linear_wl28', ReducedRegressionForecaster(LinearRegression(), window_length=28)),
    ])