import pandas as pd
from typing import Tuple
import numpy as np


def load_data(path: str) -> Tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(path, index_col=0)  # Skip the index column
    df = df.dropna()

    X = df.iloc[:, :-1].values  # YearsExperience as array
    y = df.iloc[:, -1].values   # Salary as array

    return X, y