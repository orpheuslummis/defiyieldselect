README
======

how to use this
---------------

Run: `docker-compose up --build`

With the following parameter to input in the `env.list` file:

- TIME_HORIZON= the number of timesteps in the future to compute

Uncomment the tuning container in `docker-compose.yml` to compute model search and accumulate performance data in the results volume. Suggested use: one long-running deployment for forecasting and a scalable one for hyperparameter search.


the approach
------------

Forecast a Value at a given future timestep for each swap opportunity, giving a prediction curve.

It is univariate regression: we train an estimator for each timeseries for prediction accuracy with price or APR. To compute the Value at a given time horizon, we consider both the change in value of the timeseries and the compounded interest (of the APR until up to that time). The Value is a multiplier of the latest price, eg 1.1 is a 10% increase. The predicted Value and latest price are an exponentially weighted average of their neighbors (to value in past and to mitigate accumulating error in forecasting).

Through model search, we find top (model,parameters) for each curve. Here we do 1h of computation with 4 CPU cores with a broad hyperparameter search.

The estimator for prediction is an ensemble of the top-5 models found for the timeseries. 

Deployment is through docker-compose with the following containers:

- forecasting container: fit and predict future value of swap
- modelsearch container: perform hyperparameter search
- collect_orcadefi container: every minute, collect data from collect_orcadefi API


possible directions of development
----------------------------------

- compute or improve model (hyperparameter) search
- realtime benchmarking
- online learning
- simulations with stochastic data (eg Quant GAN)
- putting into production
- neural nets 
- reinforcement learning
- data preprocessing
- obtaining better data
- trade execution engine with the various DeFI platforms/dapps
- performance
- better data - directly from blockchain