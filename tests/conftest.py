import pandas as pd
import pytest
from pytest_regressions.dataframe_regression import DataFrameRegressionFixture

from tether import Pipeline

###########################
## Testing Data Fixtures ##
###########################

@pytest.fixture
def data():
    return pd.DataFrame({
        'A': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'B': [-1.0, -0.8, -0.6, -0.4, -0.2, 0.2, 0.4, 0.6, 0.8, 1.0],
    })

##################################
## Pipeline Definition Fixtures ##
##################################


@pytest.fixture
def simple_stateless_pipeline():
    pipeline = Pipeline()

    @pipeline.step()
    def tester(data: pd.DataFrame) -> pd.DataFrame:
        data['tested'] = True
        return data
    
    return pipeline


@pytest.fixture
def simple_stateful_pipeline():
    pipeline = Pipeline()

    @pipeline.step()
    def adder(data: pd.DataFrame, fit: bool) -> pd.DataFrame:
        data['tested'] = True

        if fit:  # TODO: Save/load an actual artifact.
            data['fitted'] = 'yes'
        else:
            data['fitted'] = 'no'

        return data
    
    return pipeline


@pytest.fixture
def unordered_pipeline():
    pipeline = Pipeline()

    @pipeline.step(dependencies=['A'])
    def B(data: pd.DataFrame) -> pd.DataFrame:
        ...
        return data

    @pipeline.step()
    def A(data: pd.DataFrame) -> pd.DataFrame:
        data['tested'] = True
        return data

    @pipeline.step(dependencies=["C"])
    def C(data: pd.DataFrame) -> pd.DataFrame:
        ...
        return data
    
    return pipeline
