import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

# for now, these are the supported TIMESTEP_PERIODs
PERIOD_IN_YEARS = {
    '1d': 1/365.25,
    '1h': 1/(365.25*24),
    '1min': 1/(365.24*24*60),
}

DATA_PATH = os.getenv('DATA_PATH', 'data')
PLOTS = os.getenv('PLOTS', False)
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')
TIME_FORMAT = '%Y-%m-%d_%H_%MZ'
TIMESTEP_HORIZON = os.getenv('TIMESTEP_HORIZON', 722)
TIMESTEP_PERIOD = os.getenv('TIMESTEP_PERIOD', '1h')