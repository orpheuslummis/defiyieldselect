# we assume the data files are being updated in the background

import dataloader
import utils
from config import *
from forecast_value_univariate import forecast_pair


def run() -> dict:
    pairs = dataloader.pairs()
    predictions = {pair: forecast_pair(pair) for pair in pairs}
    return predictions


if __name__ == "__main__":
    results = run()
    print(results)
    utils.results_to_json(results)
