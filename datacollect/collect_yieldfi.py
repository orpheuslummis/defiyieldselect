"""
historical APR data from yield.fi

NOTE that this API might not be reliable in terms of data quality and future availability
"""

# TODO query only what is needed, not everything

import datetime
import itertools
import logging
import os

import pandas as pd
import requests


logging.basicConfig(level=logging.DEBUG)


API_URL = "https://api.yield.fi/lending/rate"
PATH = os.getenv(DATA_DIR, "data")
GRANULARITY = "1h"


protocols = [
    "aave",
    "compound",
    "dydx",
    "fulcrum",
]

tokens = [
    "dai",
    "eth",
    "usdc",
]


def get_yieldfi_json(protocol, asset):
    q = f"{API_URL}?protocol={protocol}&asset={asset}&granularity={GRANULARITY}"
    # if most_recent_timestamp != None: q + f"&{most_recent_timestamp}"
    j = requests.get(q).json()
    return j


if __name__ == "__main__":
    os.makedirs(PATH, exist_ok=True)
    for (protocol, token) in itertools.product(protocols, tokens):
        # query data from latest timestamp and store in or append to CSV files
        j = get_yieldfi_json(protocol, token)
        series = pd.Series(j['supply'])
        filename = f"{PATH}/{protocol}_{token}_{datetime.datetime.now().isoformat()}.csv"
        series.to_csv(filename, header=False)