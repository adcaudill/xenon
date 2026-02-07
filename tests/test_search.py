import pytest
from xenon.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_search_get(client):
    response = client.get("/search")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"input" in response.data
    assert b"Search Xenon" in response.data


def test_search_post_no_injection(client):
    response = client.post("/search", data={"query": "test"})

    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"Search Xenon" in response.data
    assert b"MySQL Error" not in response.data


def test_search_post_sql_injection(client):
    response = client.post("/search", data={"query": "'"})

    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"Search Xenon" in response.data
    assert b"MySQL Error" in response.data
    assert b"You have an error in your SQL syntax" in response.data
