import pandas as pd
from conduits import Pipeline

##########################
## Pipeline Declaration ##
##########################

pipeline = Pipeline()
pipeline["transformed"] = False


@pipeline.step(dependencies=["first_step"])
def second_step(data):
    return data + 1


@pipeline.step()
def first_step(data):
    return data ** 2


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

output = pipeline.fit_transform(df)
assert output.X.sum() != 29  # Addition before square => False!
assert output.X.sum() == 17  # Square before addition => True!
assert pipeline["transformed"] == True

pipeline.save("pipeline.joblib")

reloaded = Pipeline().load("pipeline.joblib")
assert reloaded["transformed"] == True  # State is persisted on reload.
