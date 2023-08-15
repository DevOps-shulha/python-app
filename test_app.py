import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_products(client):
    response = client.get('/api/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_product(client):
    data = {
        "name": "Test Product",
        "price": 20.0
    }
    response = client.post('/api/products', json=data)
    assert response.status_code == 201
    assert "message" in response.json
    assert "productId" in response.json

def test_get_existing_product(client):
    response = client.get('/api/products/1')
    assert response.status_code == 200
    assert "id" in response.json
    assert "name" in response.json
    assert "price" in response.json

def test_get_nonexistent_product(client):
    response = client.get('/api/products/999')
    assert response.status_code == 404
    assert "error" in response.json

def test_update_product(client):
    data = {
        "name": "Updated Product",
        "price": 25.0
    }
    response = client.patch('/api/products/1', json=data)
    assert response.status_code == 200
    assert "message" in response.json

def test_update_nonexistent_product(client):
    data = {
        "name": "Updated Product",
        "price": 25.0
    }
    response = client.patch('/api/products/999', json=data)
    assert response.status_code == 404
    assert "error" in response.json

def test_delete_product(client):
    response = client.delete('/api/products/1')
    assert response.status_code == 200
    assert "message" in response.json

def test_delete_nonexistent_product(client):
    response = client.delete('/api/products/999')
    assert response.status_code == 404
    assert "error" in response.json
