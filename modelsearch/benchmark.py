"""
inspiration from sktime benchmarking:

pipeline
results
compare results


scikit_posthocs
"""
import os

from sklearn.metrics import accuracy_score

from sktime.benchmarking.data import UEADataset, make_datasets
from sktime.benchmarking.evaluation import Evaluator
from sktime.benchmarking.metrics import PairwiseMetric
from sktime.benchmarking.orchestration import Orchestrator
from sktime.benchmarking.results import HDDResults
from sktime.benchmarking.strategies import TSCStrategy
from sktime.benchmarking.tasks import TSCTask
from sktime.classification.frequency_based import RandomIntervalSpectralForest
from sktime.classification.interval_based import TimeSeriesForest
from sktime.series_as_features.model_selection import PresplitFilesCV

# set up paths to data and results folder
import sktime

# DATA_PATH = os.path.join(os.path.dirname(sktime.__file__), "datasets/data")
DATA_PATH = "data/"
RESULTS_PATH = "results"

# Create individual pointers to dataset on the disk
datasets = [
    UEADataset(path=DATA_PATH, name="ArrowHead"),
    UEADataset(path=DATA_PATH, name="ItalyPowerDemand"),
]

tasks = [TSCTask(target="target") for _ in range(len(datasets))]

# Specify learning strategies
strategies = [
    TSCStrategy(TimeSeriesForest(n_estimators=10), name="tsf"),
    TSCStrategy(RandomIntervalSpectralForest(n_estimators=10), name="rise"),
    # TODO can it be a pipeline?
    # TODO how to define 'dummy' algorithms?
]

# Specify results object which manages the output of the benchmarking
results = HDDResults(path=RESULTS_PATH)

# run orchestrator
orchestrator = Orchestrator(
    datasets=datasets,
    tasks=tasks,
    strategies=strategies,
    cv=PresplitFilesCV(),
    results=results,
)
orchestrator.fit_predict(save_fitted_strategies=False, overwrite_predictions=True)

evaluator = Evaluator(results)
metric = PairwiseMetric(func=accuracy_score, name="accuracy")
metrics_by_strategy = evaluator.evaluate(metric=metric)
metrics_by_strategy.head()

evaluator.rank()

# evaluator.plot_boxplots()
# evaluator.ranks()
# evaluator.t_test()
# evaluator.sign_test()
# evaluator.ranksum_test()
# evaluator.t_test_with_bonferroni_correction()
# evaluator.wilcoxon_test()
# evaluator.friedman_test()
# evaluator.nemenyi()