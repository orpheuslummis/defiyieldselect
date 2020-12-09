import sklearn
from sklearn.ensemble import RandomForestRegressor
# from sktime.forecasting.arima import AutoARIMA
from sklearn.neighbors import KNeighborsRegressor
from sktime.forecasting.compose import (ReducedRegressionForecaster,
                                        TransformedTargetForecaster)
# from sktime.forecasting.ets import AutoETS
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.transformers.single_series.detrend import Deseasonalizer, Detrender
from sktime.forecasting.model_selection import SlidingWindowSplitter, ForecastingGridSearchCV
from sklearn.linear_model import Ridge, LinearRegression


forecasters = {
    # "exponential": ExponentialSmoothing,
    # "naive": NaiveForecaster,
    # "poly": PolynomialTrendForecaster,
    # "reducedregression": ReducedRegressionForecaster,
    # "theta": ThetaForecaster,
    # "transform": TransformedTargetForecaster,
    # "autoarima": AutoARIMA,
    # "autoets": AutoETS,
    # "dummy": sklearn.dummy.DummyClassifier, # FIXME might not take forecasting horizon as param
    "gridcv": ForecastingGridSearchCV,
}

forecaster_configs = {
    # "dummy": {
    #     "constant": {"strategy": "constant"},
    #     "most_frequent": {"strategy": "most_frequent"},
    #     "prior": {"strategy": "prior"},
    #     "stratified": {"strategy": "stratified"},
    #     "uniform": {"strategy": "uniform"},
    # },
    "naive": {
        "last": {"strategy": "last"},
        # "mean": {"strategy": "mean"},
        "drift": {"strategy": "drift"},
        # "drift_wl2": {"strategy": "drift", "window_length": 2},
        # "drift_wl4": {"strategy": "drift", "window_length": 4},
        # "drift_wl6": {"strategy": "drift", "window_length": 6},
        # "drift_wl8": {"strategy": "drift", "window_length": 8},
        # "drift_wl10": {"strategy": "drift", "window_length": 10},
        # "drift_wl20": {"strategy": "drift", "window_length": 20},
    },
    # ConditionalDeseasonalizer
    # "transform": {
    #     "intro_sp12": {"steps": [
    #             ("deseasonalise", Deseasonalizer(model="multiplicative", sp=12)),
    #             ("detrend", Detrender(forecaster=PolynomialTrendForecaster(degree=2))),
    #             ("forecast", ReducedRegressionForecaster(regressor=RandomForestRegressor(), window_length=12, strategy="recursive"))
    #             ],
    #     },
    #     "intro_sp60": {"steps": [
    #             ("deseasonalise", Deseasonalizer(model="multiplicative", sp=60)),
    #             ("detrend", Detrender(forecaster=PolynomialTrendForecaster(degree=2))),
    #             ("forecast", ReducedRegressionForecaster(regressor=RandomForestRegressor(), window_length=60, strategy="recursive"))
    #             ],
    #     },
    # },
    "poly": {
        # "degree1_linear": {"degree": 1, "regressor": LinearRegression()},
        "degree1_forest": {"degree": 1, "regressor": RandomForestRegressor()},
        # "degree1_ridge": {"degree": 1, "regressor": Ridge()},
        # "degree2_linear": {"degree": 2, "regressor": LinearRegression()},
        "degree2_forest": {"degree": 2, "regressor": RandomForestRegressor()},
        # "degree2_ridge": {"degree": 2, "regressor": Ridge()},
        # "degree2_ridge_alpha05": {"degree": 2, "regressor": Ridge(alpha=0.5)},
        # "degree2_ridge_alpha025": {"degree": 2, "regressor": Ridge(alpha=0.25)},
        # "degree3_linear": {"degree": 3, "regressor": LinearRegression()},
        # "degree3_forest": {"degree": 3, "regressor": RandomForestRegressor()},
    },
    "exponential": {
        "default": {},
        # "damped": {"damped": True},
        # "trend_add": {"trend": "add"},
        # "trend_mul": {"trend": "mul"},
        # "remove_bias": {"remove_bias": True},
        # "sp60": {"sp": 60},
    },
    "theta": {
        "default": {},
        # "sp80": {"sp": 80},
        # "sp100": {"sp": 100},
        # "sp40": {"sp": 40},
        # "sp60": {"sp": 60},
        "smooth05": {"smoothing_level": 0.5},
        "smooth1": {"smoothing_level": 1},
        # "smooth2": {"smoothing_level": 2},
    },
    # "autoets": {
    #     "default": {},
    # },
    # "autoarima": {
    #     "default": {},
    # }
    "reducedregression": {
        # "forest": {"regressor": RandomForestRegressor()},
        # "forest_wl20": {"regressor": RandomForestRegressor(), "window_length": 20},
        # "forest_wl30": {"regressor": RandomForestRegressor(), "window_length": 30},
        # "forest_wl100": {"regressor": RandomForestRegressor(), "window_length": 100},
        # "kneighbors1": {"regressor": KNeighborsRegressor(n_neighbors=1)},
        # "kneighbors2": {"regressor": KNeighborsRegressor(n_neighbors=2)},
        # "kneighbors2_wl10": {"regressor": KNeighborsRegressor(n_neighbors=2), "window_length": 10},
        # "kneighbors2_wl20": {"regressor": KNeighborsRegressor(n_neighbors=2), "window_length": 20},
        # "kneighbors2_wl30": {"regressor": KNeighborsRegressor(n_neighbors=2), "window_length": 30},
        # "kneighbors3": {"regressor": KNeighborsRegressor(n_neighbors=3)},
        # "kneighbors4": {"regressor": KNeighborsRegressor(n_neighbors=4)},
        # "kneighbors5": {"regressor": KNeighborsRegressor(n_neighbors=5)},
        "ridge": {"regressor": Ridge()},
        "linear": {"regressor": LinearRegression()},
    },
    "gridcv": {
        "rrrr": {
            "forecaster": ReducedRegressionForecaster(regressor=LinearRegression(), strategy="recursive"),
            "cv": SlidingWindowSplitter(initial_window=int(330 * 0.5)), #FIXME
            "param_grid": {"window_length": range(5,105,5)},
            },
        "theta": {
            "forecaster": ThetaForecaster(),
            "cv": SlidingWindowSplitter(initial_window=int(330 * 0.5)), #FIXME
            "param_grid": {"sp": range(5,105,5)},
        },
    },
}