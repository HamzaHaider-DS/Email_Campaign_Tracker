from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.services.campaign_service import (
    create_campaign_service, get_campaign_service, list_campaigns_service,
    update_campaign_service, delete_campaign_service
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post(
    "/",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
    summary="Create a campaign",
    description="Create a new email campaign for the authenticated user.",
)
async def create_campaign_endpoint(
    data: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new campaign with subject, body, and initial draft status."""
    return await create_campaign_service(db, current_user, data)


@router.get(
    "/",
    response_model=list[CampaignResponse],
    summary="List your campaigns",
    description="Return all non-deleted campaigns owned by the authenticated user.",
)
async def list_campaigns_endpoint(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List campaigns belonging to the current user."""
    return await list_campaigns_service(db, current_user, skip, limit)


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse,
    summary="Get one campaign",
    description="Fetch details for a single campaign by its ID.",
)
async def get_campaign_endpoint(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single campaign if it exists and belongs to the user."""
    return await get_campaign_service(db, current_user, campaign_id)


@router.patch(
    "/{campaign_id}",
    response_model=CampaignResponse,
    summary="Update a campaign",
    description="Modify campaign details such as subject, body, or status.",
)
async def update_campaign_endpoint(
    campaign_id: int,
    data: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing campaign."""
    return await update_campaign_service(db, current_user, campaign_id, data)


@router.delete(
    "/{campaign_id}",
    summary="Delete a campaign",
    description="Soft-delete a campaign so it no longer appears in normal listings.",
)
async def delete_campaign_endpoint(
    campaign_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft-delete a campaign using its ID."""
    return await delete_campaign_service(db, current_user, campaign_id)