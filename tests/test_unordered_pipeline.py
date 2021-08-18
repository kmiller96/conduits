import pytest
import pandas as pd

from tether import Pipeline

##############
## Fixtures ##
##############

@pytest.fixture
def unordered_pipeline():
    pipeline = Pipeline()

    @pipeline.step(dependencies=['A'])
    def B(data: pd.DataFrame) -> pd.DataFrame:
        ...
        return data

    @pipeline.step()
    def A(data: pd.DataFrame) -> pd.DataFrame:
        ...
        return data

    @pipeline.step(dependencies=["C"])
    def C(data: pd.DataFrame) -> pd.DataFrame:
        ...
        return data
    
    return pipeline

###########
## Tests ##
###########
