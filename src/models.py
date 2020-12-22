from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sktime.base import BaseEstimator
from sktime.forecasting.compose import (EnsembleForecaster,
                                        ReducedRegressionForecaster)
from sktime.regression.compose import TimeSeriesForestRegressor


F1 = EnsembleForecaster([
        ('rr_linear_wl7', ReducedRegressionForecaster(LinearRegression(), window_length=7)),
        # ('rr_linear_wl21', ReducedRegressionForecaster(LinearRegression(), window_length=21)),
        # ('rr_linear_wl28', ReducedRegressionForecaster(LinearRegression(), window_length=28)),
    ])


F2 = EnsembleForecaster([
        ('rr_linear_wl21', ReducedRegressionForecaster(LinearRegression(), window_length=21)),
        ('rr_linear_wl28', ReducedRegressionForecaster(LinearRegression(), window_length=28)),
    ])


models = {
    'f1': F1,
    'f2': F2,
}

def all_models() -> list[(str, BaseEstimator)]:
    return models.items()
