DeFi yield optimization
=======================

Three components:

- Collecting APR and price data (`collect`)
- Score each pair of curves (`score`)
- Expose the scores via a Web JSON API (`serve`)

Work done for Bowhead by Orfeo Lummis in 2021.


How to use
----------

Run locally with docker: `./run-local-docker.sh`

Run locally with kubernetes: `./run-local-k8s.sh`

Run locally without Docker (requires Python 3.8 and poetry): `poetry install; source .venv/bin/activate; python -m run`

Run remotely with kubernetes: `./run-remote-k8s.sh`

In `env.list` define the parameters:

- TBD
