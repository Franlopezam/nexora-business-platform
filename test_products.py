def auth(client):
    data = client.post("/api/auth/login", json={
        "email": "admin@test.local",
        "password": "Test123!",
    }).json()
    return {"Authorization": f"Bearer {data['access_token']}"}


def test_create_product(client):
    headers = auth(client)
    response = client.post("/api/products", headers=headers, json={
        "sku": "NX-001",
        "name": "Keyboard",
        "description": "Demo product",
        "price": 499,
        "stock": 10,
        "min_stock": 2,
    })
    assert response.status_code == 200
    assert response.json()["sku"] == "NX-001"


def test_product_list_requires_auth(client):
    response = client.get("/api/products")
    assert response.status_code == 401
