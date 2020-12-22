README
======

how to use this
---------------

Run: `docker-compose up --build`

With the following parameter to input in the `env.list` file:

- TIMESTEP_INTERVAL=1h resampling interval
- TIMESTEP_HORIZON=100 list of the future timesteps to compute, if a single integer is given treat it as range(1,n+1)

Deployment is through docker-compose with the containers:

- `forecasting`: fit and predict future value of swap
- `modelsearch`: perform hyperparameter search 
- `collect_orcadefi`: every minute, collect orcadefi data API into the data volume


the approach
------------

Forecast Value of yield token swap at a given future timestep (giving a prediction curve).

It is univariate regression: we train an estimator for each timeseries - price, apr. The Value at a given time horizon is the change in value and the compounded interest until that time horizon. The Value is a multiplier of the latest price, eg 1.1 is a 10% increase. TODO The Value and latest price are an exponentially weighted average of their neighbors (to value in past and to mitigate accumulating error in forecasting).

TODO The estimator for prediction is an ensemble of the top-5 models found for the timeseries. We performed 1h of computation with 4 CPU cores with a broad hyperparameter search to find the top (model,parameters) models for each timeseries.

The 1h default resampling interval is to allow the forecasting up to 1 month in 722 steps to be tractable (vs 43444 steps with an interval of 1min).

The reason why we don't include a target column in the data is that we fix the base multiplier (1) to be the latest data. In other words, latest data point is used as reference point (1) to calculate the target multiplier.


possible directions of development
----------------------------------

- compute or improve model (hyperparameter) search
- realtime benchmarking -- smape loss of predicted value (timestep of prediction, horizon) -> loss
- online learning
- simulations with stochastic data (eg Quant GAN)
- putting into production
- neural nets 
- reinforcement learning
- data preprocessing
- obtaining better data
- trade execution engine with the various DeFI platforms/dapps
- performance
- data directly from blockchain (API)
- one big DataFrame