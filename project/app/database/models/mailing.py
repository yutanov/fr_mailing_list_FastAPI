from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship
from app.database.models.message import MessageGet, Message


class MailingBase(SQLModel):
    __tablename__ = "mailings"

    sending_start_date: datetime = Field(
        nullable=False, default=datetime.utcnow(),
        title="Дата начала рассылки", description="Для корректной работы, используйте временную зону UTC"
    )
    sending_end_date: datetime = Field(
        nullable=False, default=datetime.utcnow(),
        title="Дата окончания рассылки", description="Для корректной работы, используйте временную зону UTC"
    )

    message_text: str = Field(
        nullable=False, default="Example Message",
        title="Сообщение которое будет отправляться клиентам"
    )
    client_filter_json: str = Field(
        nullable=False, default="{}",
        title="Json строка фильтра по которому будут выбираться клиенты",
        description="Доступные параметры: (можно совмещать)\n"
                    "\"tag\": \"ExampleTag\" -- Фильтрация по тегу\n"
                    "\"phoneOperatorCode\": \"912\" -- Фильтрация по коду мобильного оператора\n"
    )


class Mailing(MailingBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    messages: list["Message"] = Relationship(back_populates="mailing")
    logs: list["MailingLog"] = Relationship(back_populates="mailing")


class MailingGet(MailingBase):
    id: int
    sending_start_date: datetime
    sending_end_date: datetime

    message_text: str
    client_filter_json: str


class MailingGetWithMessages(MailingGet):
    messages: list["MessageGet"] = []


class MailingCreate(MailingBase):
    pass


class MailingUpdate(SQLModel):
    sending_start_date: Optional[datetime]
    sending_end_date: Optional[datetime]

    message_text: Optional[str]
    client_filter_json: Optional[str]


from app.database.models.logs.mailing_log import MailingLog

MailingGetWithMessages.update_forward_refs()