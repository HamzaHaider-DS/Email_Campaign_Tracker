from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import add_contact_service, list_contacts_service

router = APIRouter(prefix="/campaigns/{campaign_id}/contacts", tags=["Contacts"])


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    summary="Add a contact to a campaign",
    description="Add a recipient to a specific campaign and generate a tracking token for opens and clicks.",
)
async def add_contact_endpoint(
    campaign_id: int,
    data: ContactCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new contact under a campaign."""
    return await add_contact_service(db, current_user, campaign_id, data)


@router.get(
    "/",
    response_model=list[ContactResponse],
    summary="List contacts for a campaign",
    description="Retrieve all contacts associated with a specific campaign.",
)
async def list_contacts_endpoint(
    campaign_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List contacts belonging to the selected campaign."""
    return await list_contacts_service(db, current_user, campaign_id, skip, limit)