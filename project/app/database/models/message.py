from datetime import datetime
from enum import Enum, IntEnum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.utils.models_utils import enum_elements_to_string


class SendStatusEnum(IntEnum):
    sent = 0,
    fail = 1,
    success = 2


class MessageBase(SQLModel):
    __tablename__ = "messages"

    send_status: int = Field(
        nullable=False,
        title="Статус отправки", description=f"Доступные значения:\n"
                                             f"{enum_elements_to_string(SendStatusEnum)}"
    )


class Message(MessageBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())

    logs: list["MessageLog"] = Relationship(back_populates="message")

    mailing_id: Optional[int] = Field(default=None, foreign_key="mailings.id")
    mailing: Optional["Mailing"] = Relationship(back_populates="messages")

    client_id: Optional[int] = Field(default=None, foreign_key="clients.id")
    client: Optional["Client"] = Relationship(back_populates="messages")


class MessageGet(MessageBase):
    id: int
    send_status: str
    created_at: datetime


class MessageGetWithClient(MessageGet):
    client: Optional["ClientGet"]


class MessageGetWithMailing(MessageGet):
    mailing: Optional["MailingGet"]


class MessageGetWithAll(MessageGetWithClient, MessageGetWithMailing):
    pass


class MessageCreate(MessageBase):
    mailing_id: int
    client_id: int


class MessageUpdate(SQLModel):
    send_status: Optional[str]

    mailing_id: Optional[int]
    client_id: Optional[int]


from app.database.models.logs.message_log import MessageLog

from app.database.models.client import Client, ClientGet
from app.database.models.mailing import Mailing, MailingGet

MessageGetWithClient.update_forward_refs()
MessageGetWithMailing.update_forward_refs()
MessageGetWithAll.update_forward_refs()
