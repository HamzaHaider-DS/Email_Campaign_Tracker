from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.stats import CampaignStatsResponse
from app.services.stats_service import get_campaign_stats_service

router = APIRouter(prefix="/campaigns", tags=["Stats"])


@router.get("/{campaign_id}/stats", response_model=CampaignStatsResponse)
async def get_campaign_stats_endpoint(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_campaign_stats_service(db, current_user, campaign_id)