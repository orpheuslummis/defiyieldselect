## tasks

TODO unpack the concept of 'swap' to customer

TODO what the customer wants

----

TODO forecasting pipeline for yieldfi historical data

TODO forecasting pipeline for live APR data

TODO merging of pipelines

TODO ./deploy.sh

TODO  ./dl_results.sh

TODO hyperparameter search for seasonality in Theta

TODO Deseasonalizer

TODO TransformedTargetForecaster

TODO online forecasting

TODO interpreation of SMAPE loss




## log of forecaster_config tryouts with price data

meta: all of this would be more effective with an hyperparameter optimization

theta default and smooth1 are very similar

poly degree2_* and degree3_linear is pretty bad

naive drift surprisingly decent

(Theta) there is seasonality. eg using sp=60 leads to better scores

TODO holt winters ? 

TODO convergence issues:

- 


## future directions

tuning

ensembling

data transformers (eg detrending)