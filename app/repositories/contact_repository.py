from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.contact import Contact


async def create_contact(db: AsyncSession, campaign_id: int, name: str, email: str, tracking_token: str) -> Contact:
    new_contact = Contact(
        campaign_id=campaign_id,
        name=name,
        email=email,
        tracking_token=tracking_token
    )
    db.add(new_contact)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("This email is already added to this campaign")
    await db.refresh(new_contact)
    return new_contact


async def get_contacts_by_campaign(db: AsyncSession, campaign_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Contact).where(Contact.campaign_id == campaign_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_contact_by_token(db: AsyncSession, token: str) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.tracking_token == token))
    return result.scalar_one_or_none()