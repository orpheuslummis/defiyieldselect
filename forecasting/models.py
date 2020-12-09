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

forecasters = {
    # "exponential": ExponentialSmoothing,
    # "naive": NaiveForecaster,
    # "poly": PolynomialTrendForecaster,
    "reducedregression": ReducedRegressionForecaster,
    # "theta": ThetaForecaster,
    "transform": TransformedTargetForecaster,
    # "autoarima": AutoARIMA,
    # "autoets": AutoETS,
    "dummy": sklearn.dummy.DummyClassifier,
}

# commented out bad performing models
forecaster_configs = {
    "dummy": {
        "prior": {"strategy": "prior"},
    },
    "naive": {
        "last": {"strategy": "last"},
        # "mean": {"strategy": "mean"},
        "drift": {"strategy": "drift"},
        "seasonallast": {"strategy": "seasonal_last"}, 
    },
    "transform": {
        "intro_sp12": {"steps": [
                ("deseasonalise", Deseasonalizer(model="multiplicative", sp=12)),
                ("detrend", Detrender(forecaster=PolynomialTrendForecaster(degree=2))),
                ("forecast", ReducedRegressionForecaster(regressor=RandomForestRegressor(), window_length=12, strategy="recursive"))
                ],
        },
        "intro_sp60": {"steps": [
                ("deseasonalise", Deseasonalizer(model="multiplicative", sp=60)),
                ("detrend", Detrender(forecaster=PolynomialTrendForecaster(degree=2))),
                ("forecast", ReducedRegressionForecaster(regressor=RandomForestRegressor(), window_length=60, strategy="recursive"))
                ],
        },
    },
    "poly": {
        "degree1_linear": {"degree": 1, "regressor": sklearn.linear_model.LinearRegression()},
        "degree1_forest": {"degree": 1, "regressor": RandomForestRegressor()},
        "degree1_ridge": {"degree": 1, "regressor": sklearn.linear_model.Ridge()},
        # "degree2_linear": {"degree": 2, "regressor": sklearn.linear_model.LinearRegression()},
        "degree2_forest": {"degree": 2, "regressor": RandomForestRegressor()},
        # "degree2_ridge": {"degree": 2, "regressor": sklearn.linear_model.Ridge()},
        # "degree2_ridge_alpha05": {"degree": 2, "regressor": sklearn.linear_model.Ridge(alpha=0.5)},
        # "degree2_ridge_alpha025": {"degree": 2, "regressor": sklearn.linear_model.Ridge(alpha=0.25)},
        # "degree3_linear": {"degree": 3, "regressor": sklearn.linear_model.LinearRegression()},
        "degree3_forest": {"degree": 3, "regressor": RandomForestRegressor()},
    },
    "exponential": {
        "default": {},
        # "damped": {"damped": True},
        # "trend_add": {"trend": "add"},
        # "trend_mul": {"trend": "mul"},
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
        # "smooth2": {"smoothing_level": 2},
    },
    # "autoets": {
    #     "default": {},
    # },
    # "autoarima": {
    #     "default": {},
    # }
    "reducedregression": {
        "forest": {"regressor": RandomForestRegressor()},
        # "forest_wl20": {"regressor": RandomForestRegressor(), "window_length": 20},
        # "forest_wl30": {"regressor": RandomForestRegressor(), "window_length": 30},
        # "forest_wl100": {"regressor": RandomForestRegressor(), "window_length": 100},
        # "kneighbors1": {"regressor": KNeighborsRegressor(n_neighbors=1)},
        "kneighbors2": {"regressor": KNeighborsRegressor(n_neighbors=2)},
        "kneighbors3": {"regressor": KNeighborsRegressor(n_neighbors=3)},
        "kneighbors4": {"regressor": KNeighborsRegressor(n_neighbors=4)},
        "kneighbors5": {"regressor": KNeighborsRegressor(n_neighbors=5)},
        "ridge": {"regressor": sklearn.linear_model.Ridge()},
        "linear": {"regressor": sklearn.linear_model.LinearRegression()},
    },
}
