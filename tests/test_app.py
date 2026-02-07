import pytest
from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_content(client):
    response = client.get("/")
    assert b"Xenon Vulnerability Simulation Service" in response.data
    assert b"Adam Caudill" in response.data


def test_demo_cookies_set(client):
    response = client.get("/")
    cookies = response.headers.getlist("Set-Cookie")
    expected_cookies = [
        "bare_cookie=bare_value",
        "httponly_cookie=httponly_value",
        "secure_cookie=secure_value",
        "secure_httponly_cookie=secure_httponly_value",
        "lax_cookie=lax_value",
        "strict_cookie=strict_value",
        "none_cookie=none_value",
        "expiring_cookie=expiring_value",
        "path_cookie=path_value",
        "domain_cookie=domain_value",
    ]
    for expected in expected_cookies:
        assert any(expected in c for c in cookies), f"Missing cookie: {expected}"


def test_phpinfo_route(client):
    response = client.get("/phpinfo.php")
    assert response.status_code == 200
    assert b"phpinfo" in response.data or b"PHP Version" in response.data
    assert response.headers.get("X-Powered-By") == "PHP/5.0.4"
