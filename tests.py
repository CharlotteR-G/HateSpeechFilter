import pytest
from fastapi.testclient import TestClient
from main import app

# Initialize the test client
client = TestClient(app)


def test_filter_comment_empty_message():
    response = client.post("/filter", json={"message": ""})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was empty"}


def test_filter_comment_long_message():
    long_message = "a" * 256
    response = client.post("/filter", json={"message": long_message})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was too long"}


def test_filter_comment_hateful():
    hate_message = "You are an idiot"
    response = client.post("/filter", json={"message": hate_message})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was inappropriate"}


def test_filter_comment_acceptable_message():
    acceptable_message = "Have a great day!"
    response = client.post("/filter", json={"message": acceptable_message})
    assert response.status_code == 200
    assert response.json() == {"status": True, "message":
                               "Message was acceptable"}


def test_filter_comment_invalid_input():
    response = client.post("/filter", json={"wrong_key": "This is a message"})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was empty"}


def test_filter_comment_server_error():
    with pytest.raises(Exception):
        response = client.post("/filter", json={"message": "This should fail"})
        assert response.status_code == 500
