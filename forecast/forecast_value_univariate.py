"""
forecasting Price and APR curves and computing a predicted Value multiplier curve

parameterized via environment variables and data

here we want a good prediction, so we use all the available data and assume a model is already found
"""

import numpy as np
import pandas as pd

import dataloader
import models
import value
from config import *

SCORE_WINDOW = 30


def score(value_pred: pd.Series) -> float:
    return value_pred[-SCORE_WINDOW:].mean()


def forecast_pair(pair: str) -> (dict, dict):
    predictions = {}
    predictions_features = {}
    data = dataloader.get_pair_data(pair)
    forecaster = models.F1
    for feature in data.columns:
        forecaster.fit(data[feature])
        predictions_features[feature] = forecaster.predict(fh=np.arange(1, TIMESTEP_HORIZON+1))
    predictions['value'] = value.value(predictions_features)
    predictions['score'] =  score(predictions['value'])
    return predictions, predictions_features


if __name__ == "__main__":
    pairs = dataloader.list_pairs()
    predictions = {pair: forecast_pair(pair) for pair in pairs}
    print(predictions)