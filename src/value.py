import pandas as pd
import numpy as np

from config import *


def value(data: pd.DataFrame) -> pd.Series:
    '''
    we combine forecasted features (price, apr) into a value multiplier
    the base is 1, therefore a value of 1.37 means 37% increase

    output: timeseries of (value + compounded_interested(t))
    '''
    apr_multiplier = (data['apr'] * PERIOD_IN_YEARS[TIMESTEP_PERIOD]) + 1
    return apr_multiplier.cumprod() * data['price']