import json
import os
import time
from pathlib import Path

from config import *


def results_save(results: dict) -> None:
    now = int(time.time())
    os.makedirs(f'{RESULTS_DIR}/{now}', exist_ok=True)
    path = f'{RESULTS_DIR}/{now}/'

    scores = {}
    for pair in results:
        scores[pair] = results[pair]['score']
    with open(path + 'scores.json', 'w') as f:
        json.dump(scores, f)

    for pair in results:
        path_results = f'{RESULTS_DIR}/{now}/{pair}.json'

        results[pair]['value'].to_csv
        for results[pair][]

        with open(path_results, 'w') as f:
            json.dump(results, f)
