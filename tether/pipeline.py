from __future__ import annotations
from typing import Callable, Iterable
from inspect import signature
from dataclasses import dataclass

import pandas as pd
import networkx as nx
from networkx.algorithms.traversal.edgebfs import edge_bfs


class Pipeline:
    def __init__(self) -> None:
        self._dag = nx.Graph()
        self._dag.add_node("root")
        self._functions = {}

    def __call__(self, data: pd.DataFrame) -> pd.DataFrame:
        return self.transform(data)

    def _execute(self, data: pd.DataFrame, fit=False, *args, **kwargs) -> pd.DataFrame:
        data = data.copy()

        executed = set()
        for (source, dest) in edge_bfs(self._dag, source="root"):
            if dest in executed:
                continue  # Only execute each step once.
            else:
                executed.add(dest)

            print(f"Executing {dest}...")
            func = self._functions[dest]

            if "fit" not in signature(func).parameters:
                data = func(data, *args, **kwargs)
            else:
                data = func(data, fit=fit, *args, **kwargs)

        return data

    ######################
    ## Scikit Learn API ##
    ######################

    def fit(self, X: pd.DataFrame) -> Pipeline:
        self._execute(X, fit=True)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self._execute(X, fit=False)

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self.fit(X)
        return self.transform(X)

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
