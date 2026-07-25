from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.send_service import trigger_send_service

router = APIRouter(prefix="/campaigns", tags=["Send"])


@router.post(
    "/{campaign_id}/send",
    status_code=status.HTTP_200_OK,
    summary="Send a campaign",
    description="Start sending the campaign emails in the background to all contacts in the campaign.",
)
async def send_campaign_endpoint(
    campaign_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Queue a campaign send job for background processing."""
    return await trigger_send_service(db, current_user, campaign_id, background_tasks)