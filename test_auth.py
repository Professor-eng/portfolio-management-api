import pytest

async def test_register_success(client):
    response = await client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@test.com",
        "password": "password123",
    })
    assert response.status_code == 200
    assert response.json()["message"] == "New user created successfully!"


async def test_register_duplicate_username(client):
    await client.post("/auth/register", json={
        "username": "bob", "email": "bob@test.com", "password": "password123",
    })
    response = await client.post("/auth/register", json={
        "username": "bob", "email": "different@test.com", "password": "password123",
    })
    assert response.status_code == 409


async def test_login_success(client):
    await client.post("/auth/register", json={
        "username": "carol", "email": "carol@test.com", "password": "password123",
    })
    response = await client.post("/auth/login", json={
        "username": "carol", "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "username": "dave", "email": "dave@test.com", "password": "password123",
    })
    response = await client.post("/auth/login", json={
        "username": "dave", "password": "wrongpassword",
    })
    assert response.status_code == 401