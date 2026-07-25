from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.campaign_repository import get_campaign_by_id, update_campaign
from app.repositories.contact_repository import get_contacts_by_campaign
from app.models.event import Event, EventType
from app.core.mail import send_email
from app.models.user import User


async def send_campaign_background(db: AsyncSession, campaign_id: int):
    campaign = await get_campaign_by_id(db, campaign_id, user_id=None)  # see note below
    contacts = await get_contacts_by_campaign(db, campaign_id, skip=0, limit=10000)

    for contact in contacts:
        tracking_pixel = f'<img src="http://127.0.0.1:8000/track/open?token={contact.tracking_token}" width="1" height="1"/>'
        click_link = f'http://127.0.0.1:8000/track/click?token={contact.tracking_token}'
        html_body = f"{campaign.body}<br><a href='{click_link}'>Click here</a>{tracking_pixel}"

        try:
            await send_email(contact.email, campaign.subject, html_body)
        except Exception:
            continue  # skip failed sends, don't crash the whole batch

        event = Event(contact_id=contact.id, campaign_id=campaign_id, type=EventType.SENT)
        db.add(event)

    await update_campaign(db, campaign, {"status": "sent"})
    await db.commit()


async def trigger_send_service(db: AsyncSession, user: User, campaign_id: int, background_tasks):
    campaign = await get_campaign_by_id(db, campaign_id, user.id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    background_tasks.add_task(send_campaign_background, db, campaign_id)
    return {"detail": "Campaign send started"}