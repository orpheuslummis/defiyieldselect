import itertools
import os
from datetime import datetime
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.performance_metrics.forecasting import smape_loss
from sktime.utils.plotting import plot_series

import datautil
import models
from config import *


if __name__ == "__main__":
    timeseries_pairs = datautil.load_data_memoized('bowhead_prices')
    
    forecasters = models.forecasters
    forecaster_configs = models.forecaster_configs

    results = {pair: {} for pair in timeseries_pairs}
    results_paramsearch = {}
    results_path = f"{RESULTS_DIR}/results_{datetime.utcnow().strftime(TIME_FORMAT)}"
    os.makedirs(results_path, exist_ok=True)

    for forecaster_name in forecasters:
        forecaster_combinations = itertools.product(timeseries_pairs, forecaster_configs[forecaster_name])
        for p in forecaster_combinations:
            # print(forecaster_name, *p)
            # t_start = time.time()
            
            pair = p[0]
            timeseries = timeseries_pairs[pair]
            x_train, x_test = temporal_train_test_split(timeseries)

            forecaster_config_name = p[1]
            forecaster_config = forecaster_configs[forecaster_name][p[1]]
            forecaster = forecasters[forecaster_name](**forecaster_config)
            print(f"{x_test=}")
            horizon = np.arange(len(x_test)) + 1
            forecaster.fit(x_train, fh=horizon)
            x_pred = forecaster.predict()
            results[pair][f"{forecaster_name}_{forecaster_config_name}"] = smape_loss(x_test, x_pred)
            results_paramsearch[f"{forecaster_name}_{forecaster_config_name}"] = forecaster.cv_results_  

            # print(time.time()-t_start, "seconds")
            # print(pd.DataFrame(forecaster.cv_results_))

            if os.getenv("PLOTS") == "True":
                plot_series(x_train, x_test, x_pred, labels=["x_train", "x_test", "x_pred"])
                plt.title(f"{pair} {forecaster_name} {forecaster_config_name}")
                plt.savefig(f"{results_path}/{forecaster_name}_{forecaster_config_name}_{pair}_{datetime.utcnow().strftime(TIME_FORMAT)}.png")
                plt.close()

    pd.DataFrame.from_dict(results).to_json(f"{results_path}/results.json", indent=4)
    pd.DataFrame.from_dict(results_paramsearch).to_json(f"{results_path}/results_paramsearch.json", indent=4)
