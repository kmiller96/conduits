import pandas as pd
import pytest

@pytest.fixture
def data():
    return pd.DataFrame({
        'A': range(10, 100, 10),
        'B': range(-1, 1, 0.2),
    })