from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.mailing import Mailing, MailingCreate, MailingUpdate
from app.utils.models_utils import update_model


class MailingsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[Mailing]:
        query = select(Mailing).options(selectinload(Mailing.messages)).options(selectinload(Mailing.logs))
        execute = await self.session.execute(query)

        db_models: list[Mailing] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> Optional[Mailing]:
        query = select(Mailing).where(Mailing.id == model_id).options(selectinload(Mailing.messages)).options(selectinload(Mailing.logs))
        execute = await self.session.execute(query)

        db_model: Optional[Mailing] = execute.scalar_one_or_none()
        return db_model

    async def get_by_date_activation(self, current_date) -> list[Mailing]:
        query = select(Mailing).where(
            Mailing.sending_start_date <= current_date, current_date <= Mailing.sending_end_date).options(selectinload(Mailing.messages)).options(selectinload(Mailing.logs))
        execute = await self.session.execute(query)

        db_models: list[Mailing] = execute.scalars().all()
        return db_models

    def create(self, model_create: MailingCreate) -> Mailing:
        db_model = Mailing.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: Mailing, model_update: MailingUpdate) -> Mailing:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: Mailing) -> None:
        if len(db_model.logs) != 0:
            db_model.logs.clear()

        if len(db_model.messages) != 0:
            db_model.messages.clear()
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: Mailing):
        await self.session.refresh(db_model)
