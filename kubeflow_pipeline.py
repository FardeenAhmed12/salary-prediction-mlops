from kfp import dsl
from kfp.dsl import component
from kfp.compiler import Compiler


@component(base_image="python:3.11")
def load_data():
    import pandas as pd

    data = pd.read_csv("data/salary_data.csv")

    print("Dataset loaded successfully")
    print(data.head())


@component(base_image="python:3.11")
def preprocess_data():
    print("Preprocessing salary dataset...")


@component(base_image="python:3.11")
def train_model():
    import mlflow
    import pandas as pd

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    mlflow.set_tracking_uri("http://13.234.115.102:5000")
    mlflow.set_experiment("kubeflow-salary-pipeline")

    data = pd.read_csv("data/salary_data.csv")

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    with mlflow.start_run():

        model = LinearRegression()

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"MSE: {mse}")
        print(f"MAE: {mae}")
        print(f"R2 Score: {r2}")

        mlflow.log_param("model_type", "LinearRegression")

        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2_score", r2)


@component(base_image="python:3.11")
def evaluate_model():
    print("Evaluating ML model...")


@dsl.pipeline(
    name="salary-prediction-pipeline",
    description="Kubeflow ML pipeline with MLflow integration"
)
def salary_pipeline():

    load_task = load_data()

    preprocess_task = preprocess_data().after(load_task)

    train_task = train_model().after(preprocess_task)

    evaluate_model().after(train_task)


if __name__ == "__main__":

    Compiler().compile(
        pipeline_func=salary_pipeline,
        package_path="salary_pipeline.yaml"
    )
