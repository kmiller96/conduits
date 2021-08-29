import pickle
from uuid import uuid4
from tempfile import NamedTemporaryFile
from pathlib import Path

import pandas as pd
import pytest
from pytest_regressions.dataframe_regression import DataFrameRegressionFixture

from conduits import Pipeline

###########################
## Testing Data Fixtures ##
###########################


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "A": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "B": [-1.0, -0.8, -0.6, -0.4, -0.2, 0.2, 0.4, 0.6, 0.8, 1.0],
        }
    )


##################################
## Pipeline Definition Fixtures ##
##################################


@pytest.fixture
def simple_stateless_pipeline():
    pipeline = Pipeline()

    @pipeline.step()
    def tester(data: pd.DataFrame) -> pd.DataFrame:
        data["tested"] = True
        return data

    return pipeline


@pytest.fixture(scope="class")
def simple_stateful_pipeline():
    tmp_path = Path(NamedTemporaryFile().name)
    pipeline = Pipeline()

    @pipeline.step()
    def adder(data: pd.DataFrame, fit: bool, transform: bool) -> pd.DataFrame:
        data["tested"] = True

        if fit:
            with open(tmp_path, "wb") as f:
                pickle.dump("something serialised", f)

        if transform:
            with open(tmp_path, "rb") as f:
                data["fitted_value"] = pickle.load(f)

        return data

    return pipeline


@pytest.fixture
def unordered_stateless_pipeline():
    pipeline = Pipeline()

    @pipeline.step()
    def base(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] = "."
        return data

    @pipeline.step(dependencies=["A"])
    def B(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "B"
        return data

    @pipeline.step(dependencies=["base"])
    def A(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "A"
        return data

    @pipeline.step(dependencies=["B"])
    def C(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "C"
        return data

    return pipeline


@pytest.fixture(scope="class")
def unordered_stateful_pipeline():
    tmp_path = Path(NamedTemporaryFile().name)
    pipeline = Pipeline()

    @pipeline.step()
    def base(data: pd.DataFrame, fit: bool, transform: bool) -> pd.DataFrame:
        if fit:
            with open(tmp_path, "wb") as f:
                pickle.dump(".", f)

        if transform:
            with open(tmp_path, "rb") as f:
                data["string"] = pickle.load(f)

        return data

    @pipeline.step(dependencies=["A"])
    def B(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "B"
        return data

    @pipeline.step(dependencies=["base"])
    def A(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "A"
        return data

    @pipeline.step(dependencies=["B"])
    def C(data: pd.DataFrame) -> pd.DataFrame:
        data["string"] += "C"
        return data

    return pipeline
