import pandas as pd
import numpy as np

from config import *


def value(data: pd.DataFrame) -> pd.Series:
    apr_multiplier = (data['apr'] * PERIOD_IN_YEARS[TIMESTEP_PERIOD]) + 1
    value_pred = apr_multiplier.cumprod() * data['price']
    return value_pred