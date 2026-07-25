from fastapi import APIRouter, Depends
from fastapi.responses import Response, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.tracking_service import track_event_service
from app.models.event import EventType

router = APIRouter(prefix="/track", tags=["Tracking"])

# 1x1 transparent GIF, minimal valid image
TRANSPARENT_PIXEL = bytes.fromhex(
    "47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b"
)


@router.get(
    "/open",
    summary="Track an email open",
    description="Record that a contact opened the email. This endpoint returns a tiny transparent pixel used by email clients.",
)
async def track_open(token: str, db: AsyncSession = Depends(get_db)):
    """Record an open event for a contact and return a 1x1 transparent pixel."""
    await track_event_service(db, token, EventType.OPEN)
    return Response(content=TRANSPARENT_PIXEL, media_type="image/gif")


@router.get(
    "/click",
    summary="Track an email click",
    description="Record that a contact clicked the campaign link and redirect them to the destination URL.",
)
async def track_click(token: str, db: AsyncSession = Depends(get_db)):
    """Record a click event for a contact and redirect to the target URL."""
    await track_event_service(db, token, EventType.CLICK)
    return RedirectResponse(url="https://example.com")