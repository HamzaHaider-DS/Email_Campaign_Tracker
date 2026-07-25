import pytest
import uuid


async def setup_campaign(client) -> tuple[dict, int]:
    email = f"contact_{uuid.uuid4().hex[:8]}@example.com"
    await client.post("/auth/register", json={"email": email, "password": "testpass123"})
    login_response = await client.post("/auth/login", json={"email": email, "password": "testpass123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    campaign_response = await client.post("/campaigns/", json={
        "name": "Contact Test Campaign",
        "subject": "Hi",
        "body": "Body"
    }, headers=headers)
    campaign_id = campaign_response.json()["id"]

    return headers, campaign_id


@pytest.mark.asyncio
async def test_add_contact(client):
    headers, campaign_id = await setup_campaign(client)

    response = await client.post(f"/campaigns/{campaign_id}/contacts/", json={
        "name": "jane doe",
        "email": "jane@example.com"
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"  # normalized by validator
    assert "tracking_token" in data


@pytest.mark.asyncio
async def test_duplicate_contact_email_rejected(client):
    headers, campaign_id = await setup_campaign(client)

    await client.post(f"/campaigns/{campaign_id}/contacts/", json={
        "name": "Duplicate",
        "email": "dupe@example.com"
    }, headers=headers)

    second_response = await client.post(f"/campaigns/{campaign_id}/contacts/", json={
        "name": "Duplicate Again",
        "email": "dupe@example.com"
    }, headers=headers)

    assert second_response.status_code == 400