import pandas as pd
import datetime

import datamanager


assets = [
    "eth",
    "dai"
]

protocols = [
    "compound",
    "aave",
    "dydx"
]


def a_few_stats(timeseries: pd.Series):
    return {
        "len": len(timeseries),
        "autocorr": timeseries.autocorr(),
        # "pct_change": timeseries.pct_change(),
        "initial_datetime": datetime.datetime.fromtimestamp(timeseries[0][0]),
    }


if __name__ == "__main__":
    pairsdf = datamanager.obtain(protocols, assets) # pairs like (protocol, asset)

    # for now let's just say we wanna 'go to' the option with the highest autocorrelation
    # list of dicts, i want to find the key with a max value
    d = {pair: stats[pair]['autocorr'] for pair in stats}
    max_pair = max(d, key=d.get)
    # print(max_pair, stats[max_pair])
    print(f"therefore we go to {max_pair}")


    # MOVEMENT
    print(f"""
    status quo: {asset_from}
    direction: {asset_direction}
    """)

    