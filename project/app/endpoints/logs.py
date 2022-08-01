from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.logs.client_log import ClientLogGet
from app.database.models.logs.mailing_log import MailingLogGet
from app.database.models.logs.message_log import MessageLogGet
from app.database.repositories.logs.client_logs_repository import ClientLogsRepository
from app.database.repositories.logs.mailings_logs_repository import MailingsLogsRepository
from app.database.repositories.logs.messages_logs_repository import MessagesLogsRepository

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/clients", response_model=List[ClientLogGet])
async def get_clients_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с клиентами """
    client_logs_repository = ClientLogsRepository(session)

    db_logs = await client_logs_repository.get_all()

    return db_logs


@router.get("/clients/{client_id}", response_model=List[ClientLogGet])
async def get_client_logs(client_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с клиентом по ID клиента """
    client_logs_repository = ClientLogsRepository(session)

    db_logs = await client_logs_repository.get_all_by_client_id(client_id)

    return db_logs


@router.get("/mailings", response_model=List[MailingLogGet])
async def get_mailings_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с рассылками """
    mailing_logs_repository = MailingsLogsRepository(session)

    db_logs = await mailing_logs_repository.get_all()

    return db_logs


@router.get("/mailings/{mailing_id}", response_model=List[MailingLogGet])
async def get_mailing_logs(mailing_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с рассылкой по ID рассылки """
    mailings_logs_repository = MailingsLogsRepository(session)

    db_logs = await mailings_logs_repository.get_all_by_mailing_id(mailing_id)

    return db_logs


@router.get("/messages", response_model=List[MessageLogGet])
async def get_messages_logs(session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с сообщениями """
    messages_logs_repository = MessagesLogsRepository(session)

    db_logs = await messages_logs_repository.get_all()

    return db_logs


@router.get("/messages/{message_id}", response_model=List[MessageLogGet])
async def get_message_logs(message_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает все логи операций с сообщением по ID сообщения """
    messages_logs_repository = MessagesLogsRepository(session)

    db_logs = await messages_logs_repository.get_all_by_message_id(message_id)

    return db_logs
