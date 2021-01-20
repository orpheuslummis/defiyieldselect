.. role:: bash(code)
   :language: bash

DeFi yield optimization
=======================

Three components:

- Collecting APR and price data (:bash:`collect`)
- Score each pair of curves (:bash:`score`)
- Expose the scores via a Web JSON API (:bash:`serve`)

Work done for Bowhead by Orfeo Lummis in 2021.


How to use
----------

Run locally with docker: :bash:`./run-local-docker.sh`

Run locally with kubernetes: :bash:`./run-local-k8s.sh`

Run locally without Docker (requires Python 3.8 and poetry): :bash:`poetry install; source .venv/bin/activate; python -m run`

Run remotely with kubernetes: :bash:`./run-remote-k8s.sh`

In :bash:`env.list` define the parameters:

- TBD
