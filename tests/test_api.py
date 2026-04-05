import pytest
from datetime import datetime
import uuid

def test_register_user(client):
    test_username = f"test_{uuid.uuid4()}"
    test_email = f"test_{uuid.uuid4()}@test.com"
    response = client.post("/auth/register", json={
        "username": test_username,
        "email": test_email,
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_username
    assert data["email"] == test_email
    assert "id" in data

def test_register_duplicate_email(client):
    test_username = f"test_{uuid.uuid4()}"
    test_username2 = f"test_{uuid.uuid4()}"
    test_email = f"test_{uuid.uuid4()}@test.com"
    
    client.post("/auth/register", json={
        "username": test_username,
        "email": test_email,
        "password": "password123"
    })
    
    response = client.post("/auth/register", json={
        "username": test_username2,
        "email": test_email,
        "password": "password123"
    })
    assert response.status_code == 409

def test_login(client):
    test_username = f"test_{uuid.uuid4()}"
    test_email = f"test_{uuid.uuid4()}@test.com"
    client.post("/auth/register", json={
        "username": test_username,
        "email": test_email,
        "password": "password123"
    })
    
    response = client.post("/auth/login", json={
        "email": test_email,
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def get_auth_token(client):
    test_username = f"viewer_{uuid.uuid4()}"
    test_email = f"viewer_{uuid.uuid4()}@test.com"
    client.post("/auth/register", json={
        "username": test_username,
        "email": test_email,
        "password": "password123"
    })
    login_response = client.post("/auth/login", json={
        "email": test_email,
        "password": "password123"
    })
    return login_response.json()["access_token"]

def get_admin_token(client):
    login_response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "admin123"
    })
    if login_response.status_code == 200:
        return login_response.json()["access_token"]
    pytest.skip("Admin seed data not available")

def test_viewer_cannot_create_transaction(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/", headers=headers, json={
        "amount": 100.0,
        "type": "INCOME",
        "category": "freelance",
        "date": datetime.now().isoformat()
    })
    assert response.status_code == 403

def test_create_transaction(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/", headers=headers, json={
        "amount": 1000.0,
        "type": "INCOME",
        "category": "business",
        "date": datetime.now().isoformat()
    })
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 1000.0
    assert data["category"] == "business"

def test_create_invalid_amount(client):
    token = get_admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/", headers=headers, json={
        "amount": "not_a_number",
        "type": "INCOME",
        "category": "business",
        "date": datetime.now().isoformat()
    })
    assert response.status_code == 422

def test_get_summary(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/summary/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_income" in data
    assert "total_expense" in data

def test_get_transactions_filtered_by_type(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions/?type=INCOME", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

def test_get_transactions_filtered_by_category(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions/?category=rent", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

def test_date_filtering(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions/?date_from=2024-01-01&date_to=2024-12-31", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
