import pytest
import pandas as pd

from tether import Pipeline

##############
## Fixtures ##
##############

@pytest.fixture
def stateless_pipeline():
    ...  # TODO


@pytest.fixture
def stateful_pipeline():
    ... # TODO


###########
## Tests ##
###########

def test_sequential_pipeline_stateless(stateless_pipeline):
    ...

def test_sequential_pipeline_stateful(stateless_pipeline):
    ...