def test_login(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@test.local",
        "password": "Test123!",
    })
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@test.local",
        "password": "wrong",
    })
    assert response.status_code == 401
