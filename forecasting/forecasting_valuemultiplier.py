"""
forecasting the anticipated value of Price and APR curves

params: 

output: 

what is the value multiplier: prediction of what will be the predicted value at a given future time

"""

import logging

import numpy as np
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.naive import NaiveForecaster
from sktime.performance_metrics.forecasting import smape_loss

import dataloader

logging.basicConfig(level=logging.INFO)


def data_setup():
    data = {
        'price': dataloader.get_ts_price(),
        'apr': dataloader.get_ts_apr(),
    }
    # name matchings
    data['apr']['USDC_ETH'] = data['apr']['DUSDC']
    data['apr']['DAI_ETH'] = data['apr']['DDAI']

    # intersection of pairs that are both in data['price'] and data['apr']
    for pair in data['apr']:
        if pair in data['price']:
            train, test = temporal_train_test_split(data['price'][pair])
            data[f'{pair}_price_self.train'] = train
            data[f'{pair}_price_self.test'] = test
            train, test = temporal_train_test_split(data['apr'][pair])
            data[f'{pair}_apr_self.train'] = train
            data[f'{pair}_apr_self.test'] = test
    return data

def multiplier_price(self.train, self.pred):
    initial_price = self.train[0]
    current_price = self.pred.mean()
    return current_price / initial_price


class Predictor:
    """"""
    def predict(self):
        # or use @classmethod?
        self.


class PairAPRPredictor(Predictor):
    def __init__(self, pair, pipeline)
        self.pair = pair
        self.estimator = pipeline
        self.total_interest_rate = 1.0

    def load(self) -> None:

        
    def predict(self) -> None:
        self.train, self.test = self.load(pair)
        self.pipeline.fit(self.train)
        self.pred = pipeline.predict(fh=np.arange(1,horizon))
        
        # FIXME for now hard-coded 1h period. ideally extract period from data
        times_a_year = 24*365.25 # minutes
        for bar_interest_rate in self.pred:
            interest_rate = 1 + (bar_interest_rate / times_a_year)
            self.total_interest_rate = total_interest_rate * interest_rate
            # print(f'{balance=}, {interest_rate=}, {bar_interest_rate=}')

        return self.pred, smape_loss(self.test, self.pred)


    def total_interest(self):



class PairPrice(Predictor):
    def predict(self, pair, pipeline):
        self.train, self.test = temporal_train_test_split(data['price'][pair])
        pipeline.fit(self.train)
        self.pred = pipeline.predict(fh=np.arange(1,horizon))
        predicted_value = self.pred[-1:] # TODO exponential weighted average to fix current price
        return predicted_value, self.pred, smape_loss(self.test, self.pred)



if __name__ == "__main__":
    results = {}
    data = data_setup()
    pipeline = NaiveForecaster(strategy="last")
    price = Price()
    apr = Apr()
    for pair in data['apr']:
        if pair in data['price']:
            logging.info(f'{pair=}')
            apr = PairAPRPredictor(pair, pipeline)
            price = PairPricePredictor(pair, pipeline)
            apr.predict()
            price.predict()
            results[pair]['value'] =  apr.total_interest() * price.predicted_value()
            results[pair]['loss'] = {'apr': apr.smape_loss(), 'price': price.smape_loss()}
    return results
