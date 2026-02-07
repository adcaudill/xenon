import pytest
from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_reset_get_renders_form(client):
    response = client.get("/reset")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"Username" in response.data
    assert b"Reset Password" in response.data


def test_reset_post_invalid_user(client):
    response = client.post("/reset", data={"username": "invalid"})
    assert response.status_code == 200
    assert b"Reset Failed" in response.data
    assert b"User not found" in response.data
    assert b"alert-error" in response.data


def test_reset_post_valid_admin(client):
    response = client.post("/reset", data={"username": "admin@cheksuite-demo.com"})
    assert response.status_code == 200
    assert b"Reset Requested" in response.data
    assert b"alert-info" in response.data
    assert b"password reset link will be sent" in response.data


def test_reset_post_valid_test(client):
    response = client.post("/reset", data={"username": "test@cheksuite-demo.com"})
    assert response.status_code == 200
    assert b"Reset Requested" in response.data
    assert b"alert-info" in response.data
    assert b"password reset link will be sent" in response.data
