from __future__ import annotations
from typing import Callable, Iterable
from inspect import signature
from pathlib import Path

import pandas as pd
import networkx as nx
import joblib
from networkx.algorithms.traversal.edgebfs import edge_bfs


def assert_data_is_pandas_type(obj) -> bool:
    """Forces the user to use Pandas types in their inputs."""
    valid_types = {pd.DataFrame, pd.Series}

    is_valid = any(isinstance(obj, t) for t in valid_types)
    if not is_valid:
        raise TypeError(
            "Passed value is not of a valid type.\n"
            f"Type passed: {type(obj)}\n"
            f"Valid types: {valid_types}"
        )


class Pipeline:
    def __init__(self, verbose=False) -> None:
        self.verbose = verbose
        self.artifacts = {}

        self._dag = nx.Graph()
        self._dag.add_node("root")
        self._functions = {}

    def _execute(
        self, data: pd.DataFrame, fit=False, transform=True, *args, **kwargs
    ) -> pd.DataFrame:
        assert_data_is_pandas_type(data)
        data = data.copy()

        executed = set()
        for (source, dest) in edge_bfs(self._dag, source="root"):
            if dest in executed:
                continue  # Only execute each step once.
            else:
                executed.add(dest)

            if self.verbose:
                print(f"Executing {dest}...")

            func = self._functions[dest]
            sig = signature(func).parameters

            execution_args = [data, *args]
            execution_kwargs = kwargs

            if "fit" in sig:
                execution_kwargs["fit"] = fit

            if "transform" in sig:
                execution_kwargs["transform"] = transform

            data = func(*execution_args, **execution_kwargs)

        return data

    ######################
    ## Scikit Learn API ##
    ######################

    def fit(self, X: pd.DataFrame) -> Pipeline:
        self._execute(X, fit=True, transform=False)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self._execute(X, fit=False, transform=True)

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self.fit(X)
        return self.transform(X)

    ##############################################
    ## Artifact Serialisation / Deserialisation ##
    ##############################################

    def __getitem__(self, key):
        """Allows a user to fetch an artifact from the pipeline."""
        return self.artifacts[key]

    def __setitem__(self, key, value):
        """Allows a user to write an artifact into the pipeline."""
        self.artifacts[key] = value

    def save(self, path: Path):
        """Saves all pipeline objects into joblib files.

        Uses the artifacts property to decide what needs to be serialised. Can
        handle custom classes such as Scikit Learn estimators.
        """
        joblib.dump(self.artifacts, path)
        return self

    def load(self, path: Path):
        """Loads all pipeline objects, serialised as joblib files, into memory.

        Uses the artifacts property to decide what needs to be serialised. Can
        handle custom classes such as Scikit Learn estimators.
        """
        self.artifacts = joblib.load(path)
        return self

    ###################
    ## DAG Decorator ##
    ###################

    def step(self, dependencies=[]) -> Callable:
        """Decorator to define a new pipeline step.

        The decorator *must* be executed prior to decorating.

        Good ✔
        ```python
        @pipeline.step()
        def adder(data):
            return data + 1
        ```

        Bad ❌
        ```python
        @pipeline.step
        def adder(data):
            return data + 1
        ```
        """

        def _wrapper(func):
            self.add_step(func, dependencies=dependencies)

        return _wrapper

    ####################
    ## DAG Imperative ##
    ####################

    def add_step(self, func: Callable, dependencies: Iterable = []) -> Pipeline:
        """Adds another function into the pipeline DAG."""
        this = func.__name__
        self._functions[this] = func

        if dependencies:
            for dep in dependencies:
                self._dag.add_edge(dep, this)

        else:
            self._dag.add_edge("root", this)

        return self
