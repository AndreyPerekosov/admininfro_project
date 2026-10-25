import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("health")

    assert response.status_code == 200
    assert response.json() == {"status": 'ok'}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Сервис работает"


def test_hello_default():
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Привет, студент!"
    }


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32),
        (100, 212),
        (25, 77),
        (-40, -40),
        (36.6, 97.88),
    ],
)
def test_convert_to_fahrenheit(celsius, expected):
    response = client.get(
        "/convert-to-fahrenheit",
        params={"celsius": celsius},
    )

    assert response.status_code == 200
    assert response.json()["celsius"] == celsius
    assert response.json()["fahrenheit"] == expected


def test_password_default_length():
    response = client.get("/password")

    assert response.status_code == 200
    data = response.json()

    assert data["length"] == 16
    assert len(data["password"]) == 16


def test_password_custom_length():
    response = client.get("/password", params={"length": 24})

    assert response.status_code == 200
    data = response.json()

    assert data["length"] == 24
    assert len(data["password"]) == 24


@pytest.mark.parametrize("length", [7, 65, 0])
def test_password_invalid_length(length):
    response = client.get(
        "/password",
        params={"length": length},
    )

    assert response.status_code == 422


def test_random_default_range():
    response = client.get("/random")

    assert response.status_code == 200
    data = response.json()

    assert -100 <= data["number"] <= 100
    assert data["minimum"] == -100
    assert data["maximum"] == 100


def test_random_custom_range():
    response = client.get(
        "/random",
        params={"minimum": 5, "maximum": 10},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["minimum"] == 5
    assert data["maximum"] == 10
    assert 5 <= data["number"] <= 10


def test_random_single_value():
    response = client.get(
        "/random",
        params={"minimum": 7, "maximum": 7},
    )

    assert response.status_code == 200
    assert response.json()["number"] == 7


def test_random_invalid_range():
    response = client.get(
        "/random",
        params={"minimum": 10, "maximum": 5},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Минимум не может быть больше максимума"
    }
