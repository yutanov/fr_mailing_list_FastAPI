from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.message import Message, MessageCreate, MessageUpdate
from app.utils.models_utils import update_model


class MessagesRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[Message]:
        query = select(Message).options(selectinload(Message.client)).options(selectinload(Message.mailing)).options(selectinload(Message.logs))
        execute = await self.session.execute(query)

        db_models: list[Message] = execute.scalars().all()
        return db_models

    async def get_by_client_mailing_ids(self, client_id: int, mailing_id: int) -> Optional[Message]:
        query = select(Message).where(Message.client_id == client_id, Message.mailing_id == mailing_id).options(selectinload(Message.client)).options(
            selectinload(Message.mailing)).options(selectinload(Message.logs))
        execute = await self.session.execute(query)

        db_message: list[Message] = execute.scalar_one_or_none()
        return db_message

    async def get_by_id(self, model_id: int) -> Optional[Message]:
        query = select(Message).where(Message.id == model_id).options(selectinload(Message.client)).options(
            selectinload(Message.mailing)).options(selectinload(Message.logs))
        execute = await self.session.execute(query)

        db_model: Optional[Message] = execute.scalar_one_or_none()
        return db_model

    def create(self, model_create: MessageCreate) -> Message:
        db_model = Message.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: Message, model_update: MessageUpdate) -> Message:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: Message) -> None:
        if len(db_model.logs) != 0:
            db_model.logs.clear()

        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: Message):
        await self.session.refresh(db_model)
