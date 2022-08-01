from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.database.models.logs.log_base import LogBase


class MessageLogBase(LogBase):
    __tablename__ = "logs_messages"


class MessageLog(MessageLogBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())

    message_id: Optional[int] = Field(default=None, foreign_key="messages.id")
    message: Optional["Message"] = Relationship(back_populates="logs")


class MessageLogGet(MessageLogBase):
    id: int

    message_id: Optional[int]
    message: Optional["MessageGet"]


class MessageLogCreate(MessageLogBase):
    message_id: Optional[int]


class MessageLogUpdate(MessageLogBase):
    message_id: Optional[int]


from app.database.models.message import MessageGet, Message

MessageLogGet.update_forward_refs()
