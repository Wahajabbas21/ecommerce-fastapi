`import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. App Health Check
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# 2. Product Catalog & Public Endpoints
def test_get_products():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 3. User Registration & Login Flow
def test_user_auth_flow():
    test_email = "testregression@gmail.com"
    test_password = "SecurePassword123"
    
    reg_response = client.post("/api/v1/auth/register", json={
        "email": test_email,
        "password": test_password
    })
    assert reg_response.status_code in [201, 400]

    login_response = client.post("/api/v1/auth/login", data={
        "username": test_email,
        "password": test_password
    })
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    

# 4. Protected Route & Order Ownership Test (Unauthorized should fail)
def test_unauthorized_orders_access():
    response = client.get("/api/v1/orders/")
    assert response.status_code == 401

# 5. AI Chat / Search Endpoint Test
def test_ai_chat_endpoint():
    # Test without token or with token structure
    response = client.post("/api/v1/chat/", json={"message": "Show me phones"})
    # Should require auth or return proper payload structure
    assert response.status_code in [200, 401]