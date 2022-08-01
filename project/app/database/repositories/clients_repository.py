from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.client import Client, ClientCreate, ClientUpdate
from app.utils.models_utils import update_model


class ClientsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[Client]:
        query = select(Client).options(selectinload(Client.messages)).options(selectinload(Client.logs))
        execute = await self.session.execute(query)

        db_models: list[Client] = execute.scalars().all()
        return db_models

    async def get_all_by_filter(
            self,
            phone_operator_code: Optional[str] = None,
            tag: Optional[str] = None) -> list[Client]:
        query = select(Client).options(selectinload(Client.messages)).options(selectinload(Client.logs))

        if phone_operator_code is not None:
            query.where(Client.phone_operator_code == phone_operator_code)

        if tag is not None:
            query.where(Client.tag == tag)

        execute = await self.session.execute(query)

        db_models: list[Client] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> Optional[Client]:
        query = select(Client).where(Client.id == model_id).options(selectinload(Client.messages)).options(selectinload(Client.logs))
        execute = await self.session.execute(query)

        db_model: Optional[Client] = execute.scalar_one_or_none()
        return db_model

    def create(self, model_create: ClientCreate) -> Client:
        db_model = Client.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: Client, model_update: ClientUpdate) -> Client:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: Client) -> None:
        if len(db_model.messages) != 0:
            db_model.messages.clear()

        if len(db_model.logs) != 0:
            db_model.logs.clear()

        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: Client):
        await self.session.refresh(db_model)
