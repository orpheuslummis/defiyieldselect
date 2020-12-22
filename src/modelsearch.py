# model search experiments

import itertools
import numpy as np
from pathlib import Path

from sktime.forecasting.compose import ReducedRegressionForecaster
from sktime.forecasting.model_selection import (ForecastingGridSearchCV,
                                                SlidingWindowSplitter)
from sktime.performance_metrics.forecasting import smape_loss

import dataloader
import models


def rrf_wl() -> ForecastingGridSearchCV:
    regressor = models.basic_regressor
    forecaster = ReducedRegressionForecaster(regressor=regressor, window_length=1, strategy="recursive")
    param_grid = {"window_length": list(range(5, 50, 5))}
    cv = SlidingWindowSplitter(initial_window=int(100))  #FIXME 100
    return ForecastingGridSearchCV(forecaster, cv=cv, param_grid=param_grid)


# models we perform an hyperparameter for
M = {
    'rrf_wl': rrf_wl(),
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

    print(results)
    return results


def results_to_csvfile(path: Path, results: dict) -> None:
    ...


if __name__ == "__main__":
    run_experiments()
