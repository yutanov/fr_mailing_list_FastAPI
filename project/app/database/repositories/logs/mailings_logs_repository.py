from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.models.logs.mailing_log import MailingLog, MailingLogCreate, MailingLogUpdate
from app.utils.models_utils import update_model


class MailingsLogsRepository(object):
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_all(self) -> list[MailingLog]:
        query = select(MailingLog).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[MailingLog] = execute.scalars().all()
        return db_models

    async def get_by_id(self, model_id: int) -> Optional[MailingLog]:
        query = select(MailingLog).where(MailingLog.id == model_id).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_model: Optional[MailingLog] = execute.scalar_one_or_none()
        return db_model

    async def get_all_by_mailing_id(self, mailing_id: int) -> list[MailingLog]:
        query = select(MailingLog).where(MailingLog.mailing_id == mailing_id).options(selectinload(MailingLog.mailing))
        execute = await self.session.execute(query)

        db_models: list[MailingLog] = execute.scalars().all()
        return db_models

    def create(self, model_create: MailingLogCreate) -> MailingLog:
        db_model = MailingLog.from_orm(model_create)

        self.session.add(db_model)

        return db_model

    def update(self, db_model: MailingLog, model_update: MailingLogUpdate) -> MailingLog:
        update_model(db_model, model_update)

        self.session.add(db_model)
        return db_model

    async def delete(self, db_model: MailingLog) -> None:
        await self.session.delete(db_model)

    async def commit(self):
        await self.session.commit()

    async def refresh(self, db_model: MailingLog):
        await self.session.refresh(db_model)
