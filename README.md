# Conduits - A Declarative Pipelining Tool For Pandas
Traditional tools for declaring pipelines in Python suck. They are mostly 
imperative, and can sometimes requires that you adhere to strong contracts in
order to use them (looking at you Scikit Learn pipelines ಠ_ಠ). It is also 
usually done completely differently to the way the pipelines where developed 
during the ideation phase, requiring significate rewrite to get them to work
in the new paradigm.

Modelled off the declarative pipeline of Flask, **Conduits** aims to give you a
nicer, simpler, and more flexible way of declaring your data processing pipelines.

## Installation

```bash
pip install conduits
```

## Quickstart

```python 
import pandas as pd
from conduits import Pipeline

##########################
## Pipeline Declaration ##
##########################

pipeline = Pipeline()
pipeline["transformed"] = False


@pipeline.step(dependencies=["first_step"])
def second_step(data, *, adder=0):
    return data + adder


@pipeline.step()
def first_step(data, *, power=1):
    return data ** power 


@pipeline.step(dependencies=["second_step"])
def third_step(data, fit: bool, transform: bool):
    if transform:
        pipeline["transformed"] = True

    return data


###############
## Execution ##
###############

df = pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30]})

assert pipeline["transformed"] == False

output = pipeline.fit_transform(df, adder=1, power=2)

assert output.X.sum() != 29  # Addition before square => False!
assert output.X.sum() == 17  # Square before addition => True!
assert pipeline["transformed"] == True

pipeline.save("pipeline.joblib")

reloaded = Pipeline().load("pipeline.joblib")
assert reloaded["transformed"] == True  # State is persisted on reload.
```

## Usage Guide

### Declarations

#### Pipeline Decorator
Your pipeline is defined using a standard decorator syntax. You can wrap your
pipeline steps using the decorator:

```python
@pipeline.step()
def transformer(df):
    return df + 1
```

If there are any dependencies between your pipeline steps, you may specify these
in your decorator and they will be run prior to this step being run in the 
pipeline. If a step has no dependencies specified it will be assumed that it can
be run at any point.

```python
@pipeline.step(dependencies=["add_feature_X", "add_feature_Y"])
def combine_X_with_Y(df):
    return df.X + df.Y
```


#### Function Signature
The decorated function's signature carries all the information Conduits needs
to infer what functionality it needs to activate. You can pass in a single 
dataframe or many dataframes into the signature, and this will be carried 
through during the `fit()`, `transform()`, and `fit_transform()` calls. Hence
both function signatures would work:

```python
pipeline = Pipeline()

...

@pipeline.step()
def single_frame(data):
    return data + 1

...

df = pipeline.fit_transform(df)
```

```python
pipeline = Pipeline()

...

@pipeline.step()
def Xy_transfomer(X, y):
    return X + 1, y

...

X, y = pipeline.fit_transform(X, y)
```

You can also define hyperparameters that your function has access to by including
them in the function signature after the `*` separator (see 
[PEP 3102](https://www.python.org/dev/peps/pep-3102/)). It is recommended that
you set a default value for the hyperparameter but it is not necessary

```python
pipeline = Pipeline()

...

@pipeline.step()
def adder(data, *, n):
    return data + n

@pipeline.step()
def multiplier(data, *, m=1):
    return data * m

...

df = pipeline.fit_transform(df)  # Fail! `n` isn't passed in
df = pipeline.fit_transform(df, n=1)  # Will succeed! `n`=1, `m`=1
df = pipeline.fit_transform(df, n=1, m=2)  # Will succeed! `n`=`, `m`=2
```

#### Stateful Transformers
If your transformer is stateful, you can optionally supply the function with
`fit` and `transform` boolean arguments. They will be set as `True` when the 
appropriate method is called. Both arguments are optional and independent of 
one another (i.e. you can just have the `fit` argument without the `transform`
argument).

```python
@pipeline.step()
def stateful(data: pd.DataFrame, fit: bool, transform: bool):
    if fit:
        scaler = StandardScaler()
        pipeline["scaler"] = scaler.fit(data)
    
    if transform:
        data = pipeline["scaler"].transform(data)

    return data
```

#### Pipeline Serialisation
**You should not serialise the pipeline object itself**. Rather, you should
use the `pipeline.save(path)` and `pipeline.load(path)` to handle serialisation
and deserialisation. 

### API
Conduits attempts to mock the Scikit Learn API as best as possible. Your defined 
piplines have the standard methods of:

```python 
pipeline.fit(df)
out = pipeline.transform(df)
out = pipeline.fit_transform(df)
```

Note that for the current release you can only supply pandas dataframes or 
series objects. It will not accept numpy arrays.

You can save artifacts into the pipeline using standard dictionary notation.

```python 
pipeline["artifact"] = [1, 2, 3]
artifact = pipeline["artifact"]
```

You can serialise all artifacts within the pipeline using the `pipeline.save(path)`
and `pipeline.load(path)` methods. The pipeline will be serialised using the 
joblib library.

```python
pipeline = Pipeline()
...
pipeline.save("pipeline.joblib")
```

```python
pipeline = Pipeline().load("pipeline.joblib")
```

## Tests
In order to run the testing suite you should install the `dev.requirements.txt`
file. It comes with all the core dependencies used in testing and packaging.
Once you have your dependencies installed, you can run the tests via the target:

```bash
make tests
```

The tests rely on `pytest-regressions` to test some functionality. If you make
a change you can refresh the regression targets with:

```bash
make regressions
```
