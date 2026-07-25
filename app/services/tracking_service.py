from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.contact_repository import get_contact_by_token
from app.repositories.event_repository import get_event, create_event
from app.models.event import EventType


async def track_event_service(db: AsyncSession, token: str, event_type: EventType):
    contact = await get_contact_by_token(db, token)
    if not contact:
        return  # invalid/unknown token — silently ignore, don't leak info

    existing = await get_event(db, contact.id, event_type)
    if existing:
        return  # already logged, don't duplicate (matches your unique constraint)

    await create_event(db, contact.id, contact.campaign_id, event_type)