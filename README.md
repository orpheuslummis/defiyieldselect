# DeFI interest rate recommender

Work done for Bowhead by Orpheus Lummis in January 2021.

Three main components:

- Collecting APR and price data (`collect`)
- Score each pair of curves (`score`)
- Expose the scores via a Web JSON API (`serve`)


## How to run

Run locally with docker: `./run-local-docker.sh`

Run locally with kubernetes: `./run-local-k8s.sh`

Run locally without Docker (requires Python 3.8 and poetry): `poetry install; source .venv/bin/activate; python -m run`

Run remotely with kubernetes: `./run-remote-k8s.sh`

Define your preferred parameters in `dfo/config.py`, or leave it at the defaults. For more details see the comments in the file.


## API

HTTP GET endpoints for latest results:

- `/dfo/results/latest` for main model
- `/dfo/results/model/<model_name>/latest` for latest results of a particular model


## Implementation

Using contemporary Python with typing, scipy for linear regression, Flask for the web API, peewee as ORM, pandas for statistical and table/matrix operations, ...

All of it is specific to the price and APR data.


### Data collection

APR data obtained by polling the OrcaDeFi APR API.

Price data obtained by polling the UniswapV2 subgraph on thegraph.com.

Ethereum block timestamps are obtained by web3 with Infura as node.


### Data normalization

Scoring is done using a "scoring frame", that is both APR and Price dataframes over a past horizon.

We make it so that:

- the dataframe lengths are the same
- the price values are relative to their mean for comparability between tokens
- APR is a percentage
- the scoring frame has a integer representation of time relative to its beginning


### Architecture

Thread per component:
- `collect`: thread pool to periodically run the *datagetters* each in a thread
- `score`: periodically computing scores from data
- `serve`: exposing the results with a Flask app

### Model A (`model_a`)

Multiplication of the mean of APR values and the weighted slope of a linear regression of price values.

This is our main model.

### Model B (`model_b`)

Multiplication of the mean of APR values and a cubed slope of a linear regression of price values.

### Model C (`model_c`)

Random number baseline.


## Varia

The price data source (thegraph.com) supports at most a polling frequency of 30-60 seconds. By using a custom price API the polling frequency could be increased.

5-10% of the token price queries to thegraph.com fail, even when we purposefuly do simpler (but more) queries. The impact of this is tolerable because of the regularity of the data and the timespan of minutes we're operating on.

The `_start` field of the APR field is not used as we assume the `_stop` field is the given time of APR measurement.

Correctness is a goal here, but for the sake of time only piecemeal testing was done for tricky bits, in a different repository.
