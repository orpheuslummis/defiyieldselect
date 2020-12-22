# for each pair X (price, apr) curve
# find the best model parameters for an overall loss. like sum of smape losses of all the series.
# grid of combinations

# obtain a handful of pipelines to use in production -- find top 5 models

# named outputs of anticipated values

# use sktime benchmarking if it's ready

# visualize the graph and understand the algorithms

# how to optimize a pipeline

import os

from sklearn.metrics import accuracy_score
from sktime.benchmarking.data import UEADataset, make_datasets
from sktime.benchmarking.evaluation import Evaluator
# from sktime.benchmarking.metrics import PairwiseMetric
from sktime.benchmarking.orchestration import Orchestrator
from sktime.benchmarking.results import HDDResults
from sktime.benchmarking.strategies import TSRStrategy
from sktime.benchmarking.tasks import TSRTask
from sktime.regression.compose import TimeSeriesForestRegressor
from sktime.series_as_features.model_selection import PresplitFilesCV

from datautil import BowheadHistoricalDataset

DATA_PATH='data'
RESULTS_PATH='results1'

datasets = [ # TODO one dataset per timeseries <pair> X price X apr
    BowheadHistoricalDataset(path=f'{DATA_PATH}/bowhead/', name="bowhead")
]

strategies = [ # TODO make a strategy for all the activated models in models
    TSRStrategy(TimeSeriesForestRegressor(n_estimators=10), name="tsf"),
    # TODO models here
]

orchestrator = Orchestrator(
    datasets=datasets,
    tasks=[TSRTask(target="target") for _ in range(len(datasets))],
    strategies=strategies,
    cv=PresplitFilesCV(),
    results=HDDResults(path=RESULTS_PATH),
)
orchestrator.fit_predict(save_fitted_strategies=False, overwrite_predictions=True)

# TODO model experiments



# evaluator = Evaluator(results)
# metric = PairwiseMetric(func=accuracy_score, name="accuracy")
# metrics_by_strategy = evaluator.evaluate(metric=metric)
# metrics_by_strategy.head()

# evaluator.rank()

# evaluator.plot_boxplots()
# evaluator.ranks()
# evaluator.t_test()
# evaluator.sign_test()
# evaluator.ranksum_test()
# evaluator.t_test_with_bonferroni_correction()
# evaluator.wilcoxon_test()
# evaluator.friedman_test()
# evaluator.nemenyi()