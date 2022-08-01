from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.database.models.message import Message, MessageGetWithAll, MessageGet
from app.database.repositories.messages_repository import MessagesRepository
from app.responses import Message
from app.utils.logger_util import LoggerLevelsEnum, LoggerActionsEnum, Logger

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[MessageGet])
async def get_messages(session: AsyncSession = Depends(get_session)):
    """ Получает все сообщения. """
    messages_repository = MessagesRepository(session)

    db_messages = await messages_repository.get_all()

    return db_messages


@router.get("/{message_id}", response_model=MessageGetWithAll, responses={'404': {'model': Message}})
async def get_message(message_id: int, session: AsyncSession = Depends(get_session)):
    """ Получает сообщение по ID. """
    message_repository = MessagesRepository(session)

    db_message: Optional[Message] = await message_repository.get_by_id(message_id)
    if db_message is None:
        return JSONResponse(status_code=404, content={'message': f"[ID:{message_id}] Message not found"})

    return db_message


@router.delete("/{message_id}", responses={'404': {'model': Message}, '200': {'model': Message}})
async def delete_message(message_id: int, session: AsyncSession = Depends(get_session)):
    """ Удаляет сообщение по ID. """
    logger = Logger(session)
    message_repository = MessagesRepository(session)

    db_message: Optional[Message] = await message_repository.get_by_id(message_id)
    if db_message is None:
        await logger.create_message_log(None, LoggerLevelsEnum.error, LoggerActionsEnum.delete,
                                        f"[ID:{message_id}] Message Not Found")
        return JSONResponse(status_code=404, content={'message': f"[ID:{message_id}] Message not found"})

    await message_repository.delete(db_message)
    await message_repository.commit()

    await logger.create_message_log(None, LoggerLevelsEnum.debug, LoggerActionsEnum.delete,
                                    f"[ID:{message_id}] Message Deleted")

    return JSONResponse(status_code=200, content={'message': f'[ID:{message_id}] Message deleted successfully'})
