import itertools
import os
import shelve
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series

from config import *
import datautil
import models


if __name__ == "__main__":
    timeseries_pairs = datautil.load_data_memoized('bowhead_prices')
    
    results = {pair: {} for pair in timeseries_pairs}
    results_path = f"{RESULTS_DIR}/results_{datetime.utcnow().strftime(TIME_FORMAT)}"
    os.makedirs(results_path, exist_ok=True)

    forecasters = models.forecasters
    forecaster_configs = models.forecaster_configs

    for forecaster_name in forecasters:
        forecaster_combinations = itertools.product(timeseries_pairs, forecaster_configs[forecaster_name])
        for p in forecaster_combinations:
            print(forecaster_name, *p)
            pair = p[0]
            forecaster_config = forecaster_configs[forecaster_name][p[1]]
            forecaster_config_name = p[1]
            forecaster = forecasters[forecaster_name](**forecaster_config)
            timeseries = timeseries_pairs[pair]

            x_train, x_test = temporal_train_test_split(timeseries)
            forecaster.fit(x_train)
            horizon = np.arange(len(x_test)) + 1  # FIXME robust?
            # print(f"{horizon=}")
            x_pred = forecaster.predict(horizon)

            smape_loss_result = smape_loss(x_test, x_pred)
            results[pair][f"{forecaster_name}_{forecaster_config_name}"] = smape_loss_result    

            if os.getenv("PLOTS") == "True":
                plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
                plt.title(f"{pair} {forecaster_name} {forecaster_config_name}")
                plt.savefig(f"{results_path}/{pair}_{forecaster_name}_{forecaster_config_name}_{datetime.utcnow().strftime(TIME_FORMAT)}.png")
                plt.close()

    pd.DataFrame.from_dict(results).to_json(f"{results_path}/result.json", indent=4)
