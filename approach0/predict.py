import pandas as pd

from statistics import mean

# for each timeseries, extrapolate the line between the averages of the 4th quartiles of recent data points
# we select the highest slope as our prediction of which asset will have the highest yield
# NOTE not sure i'm talking about quartiles correctly...

# NOTE there are many other and better ways to predict

def line34(timeseries: pd.Series) -> float:
    # FIXME going from pd.Series to list. ... uuuh slicing Series
    second_half = timeseries[int(len(timeseries)/2):len(timeseries)]
    third_quartile = second_half[:int(len(second_half)/2)]
    fourth_quartile = second_half[int(len(second_half)/2):len(second_half)]
    # slope = fourth_quartile.mean() / third_quartile.mean()
    slope = mean(fourth_quartile) / mean(third_quartile)
    return slope