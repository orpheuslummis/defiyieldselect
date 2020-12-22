# we assume the data files are being updated in the background

import dataloader
from forecast_value_univariate import forecast_pair


def run() -> dict:
    pairs = dataloader.pairs()
    predictions = {pair: forecast_pair(pair) for pair in pairs}
    print(predictions)
    return predictions


if __name__ == "__main__":
    run()