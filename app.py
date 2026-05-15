from fastapi import FastAPI
from pydantic import BaseModel

from src.predict import predict_salary

app = FastAPI(title="Salary Prediction MLOps API", description="Predict employee salaries based on years of experience")


class SalaryInput(BaseModel):
    years_experience: float


@app.get("/")
def home():
    """
    API information endpoint
    """
    return {"message": "Salary Prediction API", "version": "1.0.0"}


@app.post("/predict")
def predict(data: SalaryInput):
    """
    Predict salary based on years of experience
    """
    result = predict_salary(data.years_experience)

    return {
        "predicted_salary": round(float(result), 2),
        "years_experience": data.years_experience,
        "model": "Linear Regression",
        "confidence": "High (R² = 0.90)"
    }