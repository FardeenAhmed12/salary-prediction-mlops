from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_predict():
    response = client.post(
        "/predict",
        json={"years_experience": 5}
    )

    assert response.status_code == 200