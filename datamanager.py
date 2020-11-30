import itertools
import json
import os

import query


def setup():
    os.makedirs("data/", exist_ok=True)


def obtain(protocols, assets):
    jsons = dl_jsons(protocols, assets)
    pairsdf = {}
    for pair in jsons:
        pairsdf[pair] = pd.Series(jsons[pair]['supply'])
    return pairsdf

def dl_jsons(protocols, assets):
    for (protocol, asset) in itertools.product(protocols, assets):
        with open(f"data/{protocol}_{asset}.json", 'w') as f:
            json.dump(query.get_yieldfi_rate(protocol, asset), f)


def read_jsons(protocols, assets):
    jsons = {}
    for (protocol, asset) in itertools.product(protocols, assets):
        with open(f"data/{protocol}_{asset}.json", 'r') as f:
            jsons[(protocol, asset)] = json.load(f)
    return jsons