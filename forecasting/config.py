import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

BIN_PERIOD = '1h'
# BIN_PERIOD = '1m'
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')
TIME_FORMAT = '%Y-%m-%d_%H_%MZ'