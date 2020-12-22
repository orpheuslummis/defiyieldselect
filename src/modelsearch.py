# model search experiments

import itertools
import numpy as np
from pathlib import Path
import time
import json

from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.model_selection import (ForecastingGridSearchCV,
                                                SlidingWindowSplitter)
from sktime.performance_metrics.forecasting import smape_loss
from sktime.forecasting.theta import ThetaForecaster

import dataloader
import models
from config import *

#FIXME initial_window= 


def rrf_wl() -> ForecastingGridSearchCV:
    return ForecastingGridSearchCV(
        forecaster=ReducedRegressionForecaster(regressor=models.basic_regressor, window_length=1, strategy="recursive"),
        cv=SlidingWindowSplitter(initial_window=int(100)),
        param_grid={"window_length": list(range(5, 50, 5))}
    ) # best_params = 5


def theta_sp() -> ForecastingGridSearchCV:
    return ForecastingGridSearchCV(
        forecaster=ThetaForecaster(),
        cv=SlidingWindowSplitter(initial_window=int(100)),
        param_grid={"sp": range(5,50,5)}
    ) # best_params = 


# models we perform an hyperparameter for
M = {
    'rrf_wl': rrf_wl(),
    'theta_sp': theta_sp(),
}


def run_experiments() -> dict:
    """
    train and eval for each (pair, model, feature)
    output their results: best params, smape_loss
    """
    pairs = dataloader.pairs()
    columns = ['price', 'apr']
    results = {pair: {model: {feature: {} for feature in columns} for model in M} for pair in pairs} 
    for pair in pairs:
        data_train = dataloader.get_pair_data_train(pair)
        data_test = dataloader.get_pair_data_test(pair)
        horizon = np.arange(1, len(data_test[columns[0]])+1)
        for m in M:
            for feature in columns:
                train = data_train[feature]
                test = data_test[feature]
                M[m].fit(train)
                pred = M[m].predict(X=test, fh=horizon)
                results[pair][m][feature]['best_params'] = M[m].best_params_
                results[pair][m][feature]['smape_loss'] = smape_loss(test, pred)
    return results


def results_to_json(path: Path, results: dict) -> None:
    path_results = f'{RESULTS_DIR}/{path}.json'
    print(results)
    with open(path_results, 'w') as f:
        json.dump(results, f)


if __name__ == "__main__":
    results = run_experiments()
    print(results)
    results_to_json(f'{int(time.time())}', results)