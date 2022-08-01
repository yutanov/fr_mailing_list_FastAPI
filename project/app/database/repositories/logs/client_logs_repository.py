from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.logs.client_log import ClientLog, ClientLogCreate, ClientLogUpdate
from app.utils.models_utils import update_model


class ClientLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[ClientLog]:
        query = select(ClientLog).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[ClientLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> Optional[ClientLog]:
        query = select(ClientLog).where(ClientLog.id == model_id).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_model: Optional[ClientLog] = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_client_id(self, client_id: int) -> list[ClientLog]:
        query = select(ClientLog).where(ClientLog.client_id == client_id).options(selectinload(ClientLog.client))
        execute = await self.session.execute(query)

        db_models: list[ClientLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: ClientLogCreate) -> ClientLog:
        db_model = ClientLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: ClientLog, model_update: ClientLogUpdate) -> ClientLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: ClientLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: ClientLog):
        await self.session.refresh(db_model)
