import pytest
from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ls_home_listing(client):
    response = client.post("/ping", data={"target": "127.0.0.1;ls"})
    assert response.status_code == 200
    assert b"total 24" in response.data
    assert b".bashrc" in response.data
    assert b"app" in response.data


def test_ls_with_flags(client):
    response = client.post("/ping", data={"target": "127.0.0.1;ls -latr"})
    assert response.status_code == 200
    assert b"total 24" in response.data
    assert b".bashrc" in response.data
    assert b"app" in response.data


def test_ls_app_empty(client):
    response = client.post("/ping", data={"target": "127.0.0.1;ls ./app"})
    assert response.status_code == 200
    assert b"total 0" in response.data


def test_ls_unknown_dir(client):
    response = client.post("/ping", data={"target": "127.0.0.1;ls /etc"})
    assert response.status_code == 200
    assert b"ls: cannot access '/etc': No such file or directory" in response.data


def test_ls_explicit_home(client):
    for d in [".", "./", "~", "/home/xenon", "/root", "/"]:
        response = client.post("/ping", data={"target": f"127.0.0.1;ls {d}"})
        assert response.status_code == 200
        assert b"total 24" in response.data
        assert b".bashrc" in response.data
        assert b"app" in response.data
