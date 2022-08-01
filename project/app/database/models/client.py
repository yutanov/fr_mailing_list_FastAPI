from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class ClientBase(SQLModel):
    __tablename__ = "clients"

    phone_number: str = Field(
        nullable=False, default="79121234567",
        title="Номер телефона", description="Указывайте только числа, без дополнительных знаков"
    )
    phone_operator_code: str = Field(
        nullable=False, default="912",
        title="Код мобильного оператора"
    )
    tag: str = Field(
        nullable=False, default="Male",
        title="Тег", description="Используется только для фильтра рассылки"
    )

    timezone: str = Field(
        nullable=False, default="Europe/Moscow",
        title="Временная зона"
    )


class Client(ClientBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    messages: list["Message"] = Relationship(back_populates="client")
    logs: list["ClientLog"] = Relationship(back_populates="client")


class ClientGet(ClientBase):
    id: int
    phone_number: str
    phone_operator_code: str
    tag: str

    timezone: str


class ClientGetWithMessages(ClientGet):
    messages: list["MessageGet"] = []


class ClientCreate(ClientBase):
    pass


class ClientUpdate(SQLModel):
    phone_number: Optional[str]
    phone_operator_code: Optional[str]
    tag: Optional[str]

    timezone: Optional[str]


from app.database.models.message import MessageGet, Message
from app.database.models.logs.client_log import ClientLog

ClientGetWithMessages.update_forward_refs()
