"""Asserts that the pipeline can serialise and deserialise objects."""

from pathlib import Path
import pandas as pd
import pytest

from conduits.pipeline import Pipeline

##############
## Fixtures ##
##############


class CustomClassForTesting:
    def __init__(self) -> None:
        self.cols = []

    def fit(self, X: pd.DataFrame):
        self.cols = X.columns
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X.columns = self.cols
        return X

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self.fit(X).transform(X)


@pytest.fixture
def pipeline() -> Pipeline:
    pipeline = Pipeline()
    pipeline["counter"] = 0  # Initialise initial counter.

    @pipeline.step()
    def tester(data: pd.DataFrame, fit: bool, transform: bool) -> pd.DataFrame:
        pipeline["counter"] += 1

        if fit:
            transformer = CustomClassForTesting()
            pipeline["transformer"] = transformer.fit(data)

        if transform:
            data = pipeline["transformer"].transform(data)

        return data

    return pipeline


###########
## Tests ##
###########


def test_pipline_can_add_artifacts(data: pd.DataFrame):
    pipeline = Pipeline()
    pipeline["columns"] = data.columns

    assert len(pipeline.artifacts) == 1


def test_pipline_can_retrieve_artifacts(data: pd.DataFrame):
    pipeline = Pipeline()
    pipeline["columns"] = set(data.columns)

    assert pipeline["columns"] == set(data.columns)


def test_pipeline_persists_across_runs(data: pd.DataFrame, pipeline: Pipeline):
    assert pipeline["counter"] == 0

    pipeline.fit(data)
    assert pipeline["counter"] == 1

    pipeline.transform(data)
    assert pipeline["counter"] == 2


def test_pipeline_can_serialise_custom_class_objects(
    data: pd.DataFrame, pipeline: Pipeline, tmp_path: Path
):
    pipeline.fit_transform(data)
    pipeline.save(tmp_path / "pipeline.joblib")

    new = Pipeline()
    new.load(tmp_path / "pipeline.joblib")
    assert isinstance(new["transformer"], CustomClassForTesting)
