# TODO interpretation in terms of USD profit over the test set
# TODO aggregate information across runs

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import dataloader
import forecast_value_univariate as forecast

RESULTS_DIR = 'results'


def _latest_results_file():
    ls = Path(RESULTS_DIR).glob('results_*')
    # print([f for f in ls])
    latest_folder = sorted([f for f in ls])[-1:][0]
    print(f"{latest_folder=}")
    return latest_folder / Path('result.json')


def obtain_latest_results_json():
    # the results folder must be pristine
    # TODO use file's modification time instead of file name?
    resultfile = _latest_results_file()
    with resultfile.open() as f:
        j = json.load(f)
    return j


def obtain_latest_results_dataframe():
    return pd.read_json(_latest_results_file())


def flatten_results(results):
    flat_results = {}
    for key_pair in results.keys():
        for key_forecaster_config in results[key_pair].keys():
            flat_results[f"{key_pair}_{key_forecaster_config}"] = results[key_pair][key_forecaster_config]
    return flat_results


def print_descending_loss(results):
    flat_results = flatten_results(results)
    print("results in descending order of smape loss")
    [print(v, k) for k, v in reversed(sorted(flat_results.items(), key=lambda item: item[1]))]


def plot_results(results):
    flat_results = flatten_results(results)
    plt.barh(*zip(*flat_results.items()), height=0.1), 
    # plt.show()
    plt.savefig(f"{results_path}/results.png")


def print_stats(df: pd.DataFrame):
    print("~ mean smape loss per forecaster_config, across all pairs ~")
    print(df.mean(axis=1).sort_values().to_string(), '\n')

    # print("~ mean smape loss per pair, across all forecaster_configs ~")
    # print(df.mean().sort_values().to_string(), '\n')
    

def print_results_matrix(df: pd.DataFrame):
    print("the results matrix")
    print(df.to_string())


def heatmap(df: pd.DataFrame):
    # TODO make the render nicer
    plt.pcolor(df)
    plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    plt.show()


def visualize_all() -> None:
    for pair in dataloader.list_pairs():
        # for col in data.columns:
        #     plt.title(f'{pair} {col}')
        #     data[col].plot()
        #     plt.show()
        predictions, predictions_features = forecast.forecast_pair(pair)
        predictions['value'].plot()
        plt.title(f'{pair} value')
        plt.show()
        for feature in predictions_features:
            predictions_features[feature].plot()
            plt.title(f'{pair} {feature}')
            plt.show()


if __name__ == "__main__":
    # results = obtain_latest_results_json()
    # print(flatten_results(results))
    # print_descending_loss(results)
    # print(results_distribution_per_config(results))

    # resultsdf = obtain_latest_results_dataframe()
    # print_stats(resultsdf)
    # heatmap(resultsdf)
    pass
