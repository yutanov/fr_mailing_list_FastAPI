from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.mailing import MailingCreate, MailingUpdate, Mailing, MailingGet
from app.database.repositories.mailings_repository import MailingsRepository
from app.responses import Message
from app.utils.logger_util import LoggerLevelsEnum, LoggerActionsEnum, Logger

router = APIRouter(
    prefix="/mailings",
    tags=["Mailings"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[MailingGet])
async def get_mailings(session: AsyncSession = Depends(get_session)):
    """ Получает все рассылки. """
    mailings_repository = MailingsRepository(session)

    db_mailings = await mailings_repository.get_all()

    return db_mailings


@router.get("/{mailing_id}", response_model=MailingGet, responses={'404': {'model': Message}})
async def get_mailing(mailing_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает рассылку по ID. """
    mailings_repository = MailingsRepository(session)

    db_mailing: Optional[Mailing] = await mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Mailing not found"})

    return db_mailing


@router.post("/", response_model=MailingGet)
async def add_mailing(client_create: MailingCreate, session: AsyncSession = Depends(get_session)):
    """ Добавляет рассылку. """
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing = mailings_repository.create(client_create)

    await mailings_repository.commit()
    await mailings_repository.refresh(db_mailing)

    await logger.create_mailing_log(db_mailing.id, LoggerLevelsEnum.debug, LoggerActionsEnum.create,
                                   f"[ID:{db_mailing.id}] Mailing Created")

    return db_mailing


@router.put("/{mailing_id}", response_model=MailingGet, responses={'404': {'model': Message}})
async def update_mailing(mailing_id: int, mailing_update: MailingUpdate, session: AsyncSession = Depends(get_session)):
    """ Обновляет рассылку по ID. """
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing: Optional[Mailing] = await mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        await logger.create_mailing_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                        f"[ID:{mailing_id}] Mailing Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Client not found"})

    db_mailing = mailings_repository.update(db_mailing, mailing_update)

    await mailings_repository.commit()
    await mailings_repository.refresh(db_mailing)

    await logger.create_mailing_log(db_mailing.id, LoggerLevelsEnum.debug, LoggerActionsEnum.update,
                                    f"[ID:{mailing_id}] Mailing Updated")

    return db_mailing


@router.delete("/{mailing_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
async def delete_mailing(mailing_id: int, session: AsyncSession = Depends(get_session)):
    """ Удаляет рассылку по ID. """
    logger = Logger(session)
    mailings_repository = MailingsRepository(session)

    db_mailing: Optional[Mailing] = await mailings_repository.get_by_id(mailing_id)
    if db_mailing is None:
        await logger.create_mailing_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                        f"[ID:{mailing_id}] Mailing Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{mailing_id}] Mailing not found"})

    await mailings_repository.delete(db_mailing)
    await mailings_repository.commit()

    await logger.create_mailing_log(None, LoggerLevelsEnum.debug, LoggerActionsEnum.delete,
                                    f"[ID:{mailing_id}] Mailing Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{mailing_id}] Mailing deleted successfully'})
