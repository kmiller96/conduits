"""Asserts that the declarative syntax works as expected."""

import pytest
import pandas as pd

from tether import Pipeline

##############
## Fixtures ##
##############

@pytest.fixture
def stateless():
    pipeline = Pipeline()

    @pipeline.step
    def adder(data: pd.DataFrame) -> pd.DataFrame:
        data['A+1'] = data.A + 1
        return data
    
    return pipeline


@pytest.fixture
def stateful():
    pipeline = Pipeline()

    @pipeline.step
    def adder(data: pd.DataFrame, fit: bool) -> pd.DataFrame:
        data['A+1'] = data.A + 1

        if fit:
            data['fitted'] = 'yes'
        else:
            data['fitted'] = 'no'

        return data
    
    return pipeline


###########
## Tests ##
###########

def test_simple_pipeline_stateless(stateless):
    ...