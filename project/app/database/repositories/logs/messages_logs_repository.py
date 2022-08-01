from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.logs.message_log import MessageLog, MessageLogCreate, MessageLogUpdate
from app.utils.models_utils import update_model


class MessagesLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[MessageLog]:
        query = select(MessageLog).options(selectinload(MessageLog.message))
        execute = await self.session.execute(query)

        db_models: list[MessageLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> Optional[MessageLog]:
        query = select(MessageLog).where(MessageLog.id == model_id).options(selectinload(MessageLog.message))
        execute = await self.session.execute(query)

        db_model: Optional[MessageLog] = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_message_id(self, message_id: int) -> list[MessageLog]:
        query = select(MessageLog).where(MessageLog.message_id == message_id).options(selectinload(MessageLog.message))
        execute = await self.session.execute(query)

        db_models: list[MessageLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: MessageLogCreate) -> MessageLog:
        db_model = MessageLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: MessageLog, model_update: MessageLogUpdate) -> MessageLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: MessageLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: MessageLog):
        await self.session.refresh(db_model)
