async def get_auth_headers(client, username="portuser"):
    await client.post("/auth/register", json={
        "username": username, "email": f"{username}@test.com", "password": "password123",
    })
    response = await client.post("/auth/login", json={
        "username": username, "password": "password123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_add_portfolio_item(client):
    headers = await get_auth_headers(client)
    response = await client.post("/portfolio/", json={
        "stockSymbol": "RELIANCE", "quantity": 20, "averagePrice": 1450,
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["stockSymbol"] == "RELIANCE"


async def test_get_portfolio_unauthenticated(client):
    response = await client.get("/portfolio/")
    assert response.status_code == 401


async def test_delete_nonexistent_portfolio_item(client):
    headers = await get_auth_headers(client, username="portuser2")
    response = await client.delete("/portfolio/999", headers=headers)
    assert response.status_code == 404