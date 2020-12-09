import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

BIN_PERIOD = '1h'
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')
TIME_FORMAT = '%Y-%m-%d_%H_%MZ'