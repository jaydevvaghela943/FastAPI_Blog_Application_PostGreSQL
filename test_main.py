from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test Home API
def test_home():
    response = client.get("/")

    #Check Status Code
    assert response.status_code == 200

    #Check Json
    assert response.json() == {"message": "Hello World - Pytest"}

# Test Add API
def test_add():
    response = client.get("/add?a=5&b=12")

    #Check Status Code
    assert response.status_code == 200
    
    #Check Json
    assert response.json() == {"result":17}

    
