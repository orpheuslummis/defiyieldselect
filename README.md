# DeFi yield optimization

Three components:

- Collecting APR and price data (`collect`)
- Score each pair of curves (`score`)
- Expose the scores via a Web JSON API (`serve`)

Work done for Bowhead by Orfeo Lummis in 2021.


## How to use

Run locally with docker: `./run-local-docker.sh`

Run locally with kubernetes: `./run-local-k8s.sh`

Run locally without Docker (requires Python 3.8 and poetry): `poetry install; source .venv/bin/activate; python -m run`

Run remotely with kubernetes: `./run-remote-k8s.sh`

Define your prefered parameters of the app in `dfo/config.py`, or leave it at the defaults.

Perform a HTTP GET query on the endpoint `/dfo/results/latest` to obtain latest results.


## Notes

Price information is obtained using web3 (Infura) and graphql (thegraph.com's `uniswapv2` subgraph). Because these sources support at most a polling frequency of 30-60 seconds. By using a custom price API the polling frequency could be increased.

The `_start` field of the APR field is not used as we assume 