"""Asserts that the pipeline has the correct API."""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal


def test_stateless_pipeline_is_callable(data, simple_stateless_pipeline, dataframe_regression):
    output = simple_stateless_pipeline(data)

    assert output.tested.all()
    dataframe_regression.check(output)


def test_pipeline_mocks_scikit_api(data, simple_stateful_pipeline, dataframe_regression):
    pipeline = simple_stateful_pipeline

    pipeline.fit(data)
    output1 = pipeline.transform(data)
    output2 = pipeline.fit_transform(data)

    assert_frame_equal(output1, output2)
    dataframe_regression.check(output1)
