from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC
from app.database import Base
import enum


class EventType(str, enum.Enum):
    SENT = "sent"
    OPEN = "open"
    CLICK = "click"


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (UniqueConstraint("contact_id", "type", name="uq_contact_event_type"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    type: Mapped[EventType] = mapped_column(Enum(EventType))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    contact: Mapped["Contact"] = relationship(back_populates="events")