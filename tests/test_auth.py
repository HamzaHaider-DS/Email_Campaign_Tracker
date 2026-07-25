import pytest
import uuid


@pytest.mark.asyncio
async def test_register_and_login(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    register_response = await client.post("/auth/register", json={
        "email": unique_email,
        "password": "testpass123"
    })
    assert register_response.status_code == 200
    data = register_response.json()
    assert data["email"] == unique_email
    assert "id" in data
    assert "hashed_password" not in data  # password should never leak

    login_response = await client.post("/auth/login", json={
        "email": unique_email,
        "password": "testpass123"
    })
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email_fails(client):
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"

    await client.post("/auth/register", json={"email": email, "password": "testpass123"})
    second_response = await client.post("/auth/register", json={"email": email, "password": "testpass123"})

    assert second_response.status_code == 400


@pytest.mark.asyncio
async def test_login_wrong_password_fails(client):
    email = f"wrongpw_{uuid.uuid4().hex[:8]}@example.com"
    await client.post("/auth/register", json={"email": email, "password": "correctpass123"})

    response = await client.post("/auth/login", json={"email": email, "password": "wrongpassword"})
    assert response.status_code == 401