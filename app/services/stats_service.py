from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.event_repository import get_campaign_stats_raw
from app.services.campaign_service import get_campaign_service
from app.schemas.stats import CampaignStatsResponse
from app.models.user import User


async def get_campaign_stats_service(db: AsyncSession, user: User, campaign_id: int) -> CampaignStatsResponse:
    await get_campaign_service(db, user, campaign_id)  # confirms ownership, 404s if not found/not theirs

    raw_stats = await get_campaign_stats_raw(db, campaign_id)
    return CampaignStatsResponse(**raw_stats)