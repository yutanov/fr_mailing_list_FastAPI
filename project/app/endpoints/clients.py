from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.client import ClientCreate, ClientUpdate, Client, ClientGet
from app.database.repositories.clients_repository import ClientsRepository
from app.responses import Message
from app.utils.logger_util import Logger, LoggerLevelsEnum, LoggerActionsEnum

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ClientGet])
async def get_clients(session: AsyncSession = Depends(get_session)):
    """ Получает всех клиентов. """
    clients_repository = ClientsRepository(session)

    db_clients = await clients_repository.get_all()

    return db_clients


@router.get("/{client_id}", response_model=ClientGet, responses={'404': {'model': Message}})
async def get_client(client_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает клиента по ID. """
    clients_repository = ClientsRepository(session)

    db_client: Optional[Client] = await clients_repository.get_by_id(client_id)
    if db_client is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{client_id}] Client not found"})

    return db_client


@router.post("/", response_model=ClientGet)
async def add_client(client_create: ClientCreate, session: AsyncSession = Depends(get_session)):
    """ Добавляет клиента. """
    logger = Logger(session)
    clients_repository = ClientsRepository(session)

    db_client = clients_repository.create(client_create)

    await clients_repository.commit()
    await clients_repository.refresh(db_client)

    await logger.create_client_log(db_client.id, LoggerLevelsEnum.debug, LoggerActionsEnum.create,
                                   f"[ID:{db_client.id}] Client Created")

    return db_client


@router.put("/{client_id}", response_model=ClientGet, responses={'404': {'model': Message}})
async def update_client(client_id: int, client_update: ClientUpdate, session: AsyncSession = Depends(get_session)):
    """ Обновляет клиента по ID. """
    logger = Logger(session)
    clients_repository = ClientsRepository(session)

    db_client: Optional[Client] = await clients_repository.get_by_id(client_id)
    if db_client is None:
        await logger.create_client_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.update,
                                       f"[ID:{client_id}] Client Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{client_id}] Client not found"})

    db_client = clients_repository.update(db_client, client_update)

    await clients_repository.commit()
    await clients_repository.refresh(db_client)

    await logger.create_client_log(db_client.id, LoggerLevelsEnum.debug, LoggerActionsEnum.update,
                                   f"[ID:{client_id}] Client Updated")

    return db_client


@router.delete("/{client_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
async def delete_client(client_id: int, session: AsyncSession = Depends(get_session)):
    """ Удаляет клиента по ID. """
    logger = Logger(session)
    clients_repository = ClientsRepository(session)

    db_client: Optional[Client] = await clients_repository.get_by_id(client_id)
    if db_client is None:
        await logger.create_client_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                       f"[ID:{client_id}] Client Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{client_id}] Client not found"})

    await clients_repository.delete(db_client)
    await clients_repository.commit()

    await logger.create_client_log(None, LoggerLevelsEnum.debug, LoggerActionsEnum.delete,
                                   f"[ID:{client_id}] Client Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{client_id}] Client deleted successfully'})
