import pytest

from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_get_renders_form(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_login_post_invalid_user(client):
    response = client.post("/login", data={"username": "invalid", "password": "wrong"})
    assert response.status_code == 401
    assert b"Login Failed" in response.data
    assert "session" not in response.headers.get("Set-Cookie", "")


def test_login_post_valid_admin(client):
    response = client.post(
        "/login", data={"username": "admin@example.com", "password": "admin"}
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    assert "session=" in response.headers.get("Set-Cookie", "")


def test_login_post_valid_test(client):
    response = client.post(
        "/login", data={"username": "test@example.com", "password": "test"}
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    assert "session=" in response.headers.get("Set-Cookie", "")


def test_login_post_valid_user_wrong_password(client):
    response = client.post(
        "/login", data={"username": "admin@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
    assert b"Login Failed" in response.data
    # Should not set session cookie
    assert "session=" not in response.headers.get("Set-Cookie", "")
