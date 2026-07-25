from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.campaign_repository import (
    create_campaign, get_campaign_by_id, get_campaigns,
    update_campaign, soft_delete_campaign
)
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.models.user import User


async def create_campaign_service(db: AsyncSession, user: User, data: CampaignCreate):
    return await create_campaign(db, user.id, data.name, data.subject, data.body)


async def get_campaign_service(db: AsyncSession, user: User, campaign_id: int):
    campaign = await get_campaign_by_id(db, campaign_id, user.id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


async def list_campaigns_service(db: AsyncSession, user: User, skip: int, limit: int):
    return await get_campaigns(db, user.id, skip, limit)


async def update_campaign_service(db: AsyncSession, user: User, campaign_id: int, data: CampaignUpdate):
    campaign = await get_campaign_by_id(db, campaign_id, user.id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    update_data = data.model_dump(exclude_unset=True)
    return await update_campaign(db, campaign, update_data)


async def delete_campaign_service(db: AsyncSession, user: User, campaign_id: int):
    campaign = await get_campaign_by_id(db, campaign_id, user.id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    await soft_delete_campaign(db, campaign)
    return {"detail": "Campaign deleted"}