from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event, EventType
from sqlalchemy import func, select
from app.models.contact import Contact



async def get_event(db: AsyncSession, contact_id: int, event_type: EventType) -> Event | None:
    result = await db.execute(
        select(Event).where(Event.contact_id == contact_id, Event.type == event_type)
    )
    return result.scalar_one_or_none()


async def create_event(db: AsyncSession, contact_id: int, campaign_id: int, event_type: EventType) -> Event:
    new_event = Event(contact_id=contact_id, campaign_id=campaign_id, type=event_type)
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

async def get_campaign_stats_raw(db: AsyncSession, campaign_id: int) -> dict:
    total_contacts_result = await db.execute(
        select(func.count(Contact.id)).where(Contact.campaign_id == campaign_id)
    )
    total_contacts = total_contacts_result.scalar() or 0

    async def count_event(event_type: EventType) -> int:
        result = await db.execute(
            select(func.count(Event.id)).where(
                Event.campaign_id == campaign_id,
                Event.type == event_type
            )
        )
        return result.scalar() or 0

    total_sent = await count_event(EventType.SENT)
    total_opens = await count_event(EventType.OPEN)
    total_clicks = await count_event(EventType.CLICK)

    return {
        "total_contacts": total_contacts,
        "total_sent": total_sent,
        "total_opens": total_opens,
        "total_clicks": total_clicks,
    }