from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sktime.base import BaseEstimator
from sktime.forecasting.compose import (EnsembleForecaster,
                                        ReducedRegressionForecaster)
from sktime.forecasting.theta import ThetaForecaster
from sktime.regression.compose import TimeSeriesForestRegressor

basic_regressor = LinearRegression()


F1 = EnsembleForecaster([
        ('rr_linear_wl5', ReducedRegressionForecaster(LinearRegression(), window_length=5)),
        ('theta_sp?', ThetaForecaster(sp=1)),
    ])


models = {
    'f1': F1,
}

def all_models() -> list[(str, BaseEstimator)]:
    # TODO or select all the objects that are of type Forecaster? in this module
    return models.items()
