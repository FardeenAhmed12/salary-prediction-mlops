import joblib
import pandas as pd
import numpy as np
from typing import Any

model: Any = joblib.load("models/model.pkl")


def predict_salary(years_experience: float) -> float:
    data = np.array([[years_experience]])  # Use numpy array to match training

    prediction = model.predict(data)

    return prediction[0]