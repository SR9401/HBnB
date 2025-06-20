import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_create_valid_user(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["email"] == "alice@example.com"

def test_create_user_invalid_email(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bobemail.com"
    })
    assert response.status_code == 400

def test_create_user_empty_fields(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "",
        "last_name": "",
        "email": ""
    })
    assert response.status_code == 400

def test_create_user_long_first_name(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "A" * 51,
        "last_name": "Doe",
        "email": "longname@example.com"
    })
    assert response.status_code == 400

def test_create_user_duplicate_email(client):
    # First creation
    client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "duplicate@example.com"
    })
    # Second with same email
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "duplicate@example.com"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.get_json().get("error", "")

def test_get_all_users(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_nonexistent_user(client):
    response = client.get('/api/v1/users/nonexistent-id')
    assert response.status_code == 404
