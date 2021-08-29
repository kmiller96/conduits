"""Asserts that the pipeline was successfully able to generate the correct DAG."""


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
    assert "fitted_value" not in data.columns
    assert "fitted_value" in output.columns


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
