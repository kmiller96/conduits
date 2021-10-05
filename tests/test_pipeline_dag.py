"""Asserts that the pipeline was successfully able to generate the correct DAG."""

import pandas as pd
from conduits.pipeline import Pipeline


def test_simple_stateless_pipeline(data, simple_stateless_pipeline):
    pipeline = simple_stateless_pipeline

    output = pipeline.fit_transform(data)
    assert "tested" in output.columns
    assert (output.tested).all()


def test_simple_stateless_pipeline(data, simple_stateful_pipeline):
    pipeline = simple_stateful_pipeline

    pipeline.fit(data)
    assert "fitted_value" not in data.columns

    output = pipeline.fit_transform(data)
    assert "fitted_value" not in data.columns  # Shouldn't mutate original data.
    assert "fitted_value" in output.columns  # But should be present in transformed.


def test_stateless_unordered_pipeline_executes_steps_in_order(
    data, unordered_stateless_pipeline
):
    pipeline = unordered_stateless_pipeline

    output = pipeline.fit_transform(data)
    assert (output.string == ".ABC").all()


def test_stateful_unordered_pipeline_executes_steps_in_order(
    data, unordered_stateless_pipeline
):
    pipeline = unordered_stateless_pipeline

    output = pipeline.fit_transform(data)
    assert (output.string == ".ABC").all()


def test_pipeline_accepts_multiple_positional_arguments(
    data: pd.DataFrame, simple_stateless_pipeline: Pipeline
):
    pipeline = simple_stateless_pipeline

    A, B = data[["A"]], data[["B"]]
    A_prime, B_prime = pipeline.fit_transform(A, B)

    for org, new in zip((A, B), (A_prime, B_prime)):
        assert len(org) == len(new)
        assert "tested" in new.columns
