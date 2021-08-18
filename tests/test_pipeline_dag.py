"""Asserts that the pipeline was successfully able to generate the correct DAG."""


def test_unordered_pipeline_executes_steps_in_order(data, unordered_pipeline):
    pipeline = unordered_pipeline

    output = pipeline(data)
    assert (output.string == ".ABC").all()
