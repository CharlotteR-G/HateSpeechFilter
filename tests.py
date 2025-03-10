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
    hate_message = "I hate all people from that country, they are disgusting and should be eliminated"
    response = client.post("/filter", json={"message": hate_message})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was inappropriate"}


def test_filter_comment_acceptable_message():
    response = client.post("/filter", json={"message": "I love everything"})
    assert response.status_code == 200
    assert response.json() == {"status": True, "message":
                               "Message was acceptable"}


def test_filter_comment_invalid_input():
    response = client.post("/filter", json={})
    assert response.status_code == 200
    assert response.json() == {"status": False, "message":
                               "Message was empty"}


def test_filter_comment_boundary_length():
    """Test a message exactly at the allowed length limit (255 characters)."""
    boundary_message = "a" * 255
    response = client.post("/filter", json={"message": boundary_message})
    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["message"] == "Message was acceptable"


def test_filter_comment_special_characters():
    """Test a message with special characters and symbols."""
    special_message = "Hello! This message contains special characters: @#$%^&*()_+{}[]|:;<>,.?/~`"
    response = client.post("/filter", json={"message": special_message})
    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["message"] == "Message was acceptable"


def test_filter_comment_missing_field():
    """Test request with missing 'message' field."""
    response = client.post("/filter", json={})
    assert response.status_code == 200
    assert response.json()["status"] is False
    assert response.json()["message"] == "Message was empty"


import time

def test_filter_comment_response_time():
    """Test that the API responds within a reasonable time frame."""
    start_time = time.time()
    response = client.post("/filter", json={"message": "This is a normal message for timing test."})
    end_time = time.time()
    
    assert response.status_code == 200
    # Adjust the threshold as needed based on your performance requirements
    assert end_time - start_time < 5  # Response should be under 5 seconds
