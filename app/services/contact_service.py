import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.contact_repository import create_contact, get_contacts_by_campaign
from app.services.campaign_service import get_campaign_service
from app.schemas.contact import ContactCreate
from app.models.user import User


async def add_contact_service(db: AsyncSession, user: User, campaign_id: int, data: ContactCreate):
    # confirms the campaign exists AND belongs to this user (reuses Step 10 logic)
    await get_campaign_service(db, user, campaign_id)

    tracking_token = secrets.token_urlsafe(16)

    try:
        return await create_contact(db, campaign_id, data.name, data.email, tracking_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def list_contacts_service(db: AsyncSession, user: User, campaign_id: int, skip: int, limit: int):
    await get_campaign_service(db, user, campaign_id)
    return await get_contacts_by_campaign(db, campaign_id, skip, limit)