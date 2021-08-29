"""Asserts that the pipeline has the correct API."""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal


def test_pipeline_mocks_scikit_api(
    data, simple_stateful_pipeline, dataframe_regression
):
    pipeline = simple_stateful_pipeline

    pipeline.fit(data)
    output1 = pipeline.transform(data)
    output2 = pipeline.fit_transform(data)

    assert_frame_equal(output1, output2)
    dataframe_regression.check(output1)


@pytest.mark.parametrize("obj", [[1, 2, 3], "hello", {10, 20}, {"name": "bob"}])
def test_pipeline_only_accepts_pandas(obj, simple_stateful_pipeline):
    pipeline = simple_stateful_pipeline

    with pytest.raises(TypeError):
        pipeline.fit(obj)


class TestFitTransformStateManagement:
    def test_pipeline_fit_independently(self, data, simple_stateful_pipeline):
        simple_stateful_pipeline.fit(data)

    def test_pipeline_transform_independently(
        self, data, simple_stateful_pipeline, dataframe_regression
    ):
        output = simple_stateful_pipeline.transform(data)
        dataframe_regression.check(output)
