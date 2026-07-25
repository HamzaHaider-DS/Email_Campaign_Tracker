import pytest
import uuid


async def get_auth_headers(client) -> dict:
    email = f"camp_{uuid.uuid4().hex[:8]}@example.com"
    await client.post("/auth/register", json={"email": email, "password": "testpass123"})
    login_response = await client.post("/auth/login", json={"email": email, "password": "testpass123"})
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_and_get_campaign(client):
    headers = await get_auth_headers(client)

    create_response = await client.post("/campaigns/", json={
        "name": "Test Campaign",
        "subject": "Hello",
        "body": "Test body"
    }, headers=headers)
    assert create_response.status_code == 200
    campaign = create_response.json()
    assert campaign["status"] == "draft"

    get_response = await client.get(f"/campaigns/{campaign['id']}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test Campaign"


@pytest.mark.asyncio
async def test_campaign_requires_auth(client):
    response = await client.post("/campaigns/", json={
        "name": "No Auth",
        "subject": "Test",
        "body": "Test"
    })
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_soft_delete_hides_campaign(client):
    headers = await get_auth_headers(client)

    create_response = await client.post("/campaigns/", json={
        "name": "To Delete",
        "subject": "Bye",
        "body": "Deleting this"
    }, headers=headers)
    campaign_id = create_response.json()["id"]

    delete_response = await client.delete(f"/campaigns/{campaign_id}", headers=headers)
    assert delete_response.status_code == 200

    get_response = await client.get(f"/campaigns/{campaign_id}", headers=headers)
    assert get_response.status_code == 404  # soft-deleted, should look "not found"