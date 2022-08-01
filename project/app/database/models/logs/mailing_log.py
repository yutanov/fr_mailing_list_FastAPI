from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.database.models.logs.log_base import LogBase


class MailingLogBase(LogBase):
    __tablename__ = "logs_mailings"


class MailingLog(MailingLogBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())

    mailing_id: Optional[int] = Field(default=None, foreign_key="mailings.id")
    mailing: Optional["Mailing"] = Relationship(back_populates="logs")


class MailingLogGet(MailingLogBase):
    id: int
    mailing_id: Optional[int]
    mailing: Optional["MailingGet"]


class MailingLogCreate(MailingLogBase):
    mailing_id: Optional[int]


class MailingLogUpdate(MailingLogBase):
    mailing_id: Optional[int]

from app.database.models.mailing import MailingGet, Mailing


MailingLogGet.update_forward_refs()
