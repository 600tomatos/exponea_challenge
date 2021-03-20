import sys
import pytest

from os.path import abspath
from os.path import dirname as d
from multiprocessing import Event

sys.path.extend([d(d(abspath(__file__))), d(abspath(__file__))])

# How many requests will be triggered in parallel
PARALLEL_EXECUTOR_PROCESSES = 8

# How many second process will be alive
EXECUTOR_TIMEOUT = 5


@pytest.fixture
def app():
    from app import app
    return app


@pytest.fixture
def base_url():
    return 'http://0.0.0.0:5000'


@pytest.fixture
def multiproc_event():
    event = Event()
    yield event
    # Make sure we always close parallel processes
    if not event.is_set():
        event.set()


@pytest.fixture
def parallel_procs_num():
    return PARALLEL_EXECUTOR_PROCESSES


@pytest.fixture
def executor_timeout():
    return EXECUTOR_TIMEOUT
