import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

RESULTS_DIR = 'results'


def _latest_results_file():
    ls = Path(RESULTS_DIR).glob('results_*')
    latest_folder = sorted([f for f in ls])[-1:][0]
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


def results_distribution_per_config(results):
    pass


def print_stats(df: pd.DataFrame):
    # print("rows")
    # [print(row) for row in df.]

    print("~ mean loss per pair, accross all forecaster_config ~")
    print(df.mean().sort_values(), '\n')

    print("~ mean loss per forecaster_config ~")
    print(df.mean(axis=1).sort_values(), '\n')


if __name__ == "__main__":
    # results = obtain_latest_results_json()

    # print(flatten_results(results))

    # print_descending_loss(results)

    # print(results_distribution_per_config(results))

    resultsdf = obtain_latest_results_dataframe()
    print_stats(resultsdf)