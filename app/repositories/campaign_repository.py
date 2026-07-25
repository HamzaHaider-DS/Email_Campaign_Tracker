from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, UTC
from app.models.campaign import Campaign


async def create_campaign(db: AsyncSession, user_id: int, name: str, subject: str, body: str) -> Campaign:
    new_campaign = Campaign(user_id=user_id, name=name, subject=subject, body=body)
    db.add(new_campaign)
    await db.commit()
    await db.refresh(new_campaign)
    return new_campaign


async def get_campaign_by_id(db: AsyncSession, campaign_id: int, user_id: int | None = None) -> Campaign | None:
    conditions = [Campaign.id == campaign_id, Campaign.deleted_at.is_(None)]
    if user_id is not None:
        conditions.append(Campaign.user_id == user_id)
    result = await db.execute(select(Campaign).where(*conditions))
    return result.scalar_one_or_none()


async def get_campaigns(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Campaign).where(
            Campaign.user_id == user_id,
            Campaign.deleted_at.is_(None)
        ).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_campaign(db: AsyncSession, campaign: Campaign, update_data: dict) -> Campaign:
    for key, value in update_data.items():
        setattr(campaign, key, value)
    campaign.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(campaign)
    return campaign


async def soft_delete_campaign(db: AsyncSession, campaign: Campaign) -> None:
    campaign.deleted_at = datetime.now(UTC)
    await db.commit()