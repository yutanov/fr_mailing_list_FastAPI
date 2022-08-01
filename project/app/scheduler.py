import asyncio
import datetime
import json
import os

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.database import engine
from app.database.models.message import MessageCreate, SendStatusEnum, MessageUpdate
from app.database.repositories.clients_repository import ClientsRepository
from app.database.repositories.mailings_repository import MailingsRepository
from app.database.repositories.messages_repository import MessagesRepository
from app.utils.logger_util import Logger, LoggerLevelsEnum, LoggerActionsEnum


class SchedulerService:
    def __init__(self):
        self.queue = None
        self.scheduler = None

    async def check_mailings(self):
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as database_session:
            logger = Logger(database_session)
            mailings_repository = MailingsRepository(database_session)
            messages_repository = MessagesRepository(database_session)
            clients_repository = ClientsRepository(database_session)

            mailings = await mailings_repository.get_by_date_activation(datetime.datetime.utcnow())
            if len(mailings) == 0:
                return

            for mailing in mailings:
                client_filter: dict = json.loads(mailing.client_filter_json)
                clients = await clients_repository.get_all_by_filter(
                    client_filter.get("phoneOperatorCode"), client_filter.get("tag")
                )

                if len(clients) == 0:
                    continue

                for client in clients:
                    # В случае если клиентов слишком много, отправка запросов может занять некоторое время, за которое
                    # срок рассылки может закончится.
                    if mailing.sending_end_date <= datetime.datetime.utcnow():
                        break

                    # В случае если клиенту уже отравили рассылку, второй раз мы отправлять её не будем.
                    # Но если клиенту уже отправили рассылку и отправка рассылки провалилась, то мы пробуем ещё раз.
                    temp_message = await messages_repository.get_by_client_mailing_ids(client.id, mailing.id)
                    if temp_message is not None and temp_message.send_status != SendStatusEnum.fail:
                        continue

                    async with aiohttp.ClientSession() as client_session:
                        message_create = MessageCreate(
                            mailing_id=mailing.id, client_id=client.id,
                            send_status=int(SendStatusEnum.sent)
                        )

                        db_message = messages_repository.create(message_create)
                        await messages_repository.commit()
                        await messages_repository.refresh(db_message)

                        headers = {'authorization': f'Bearer {os.environ.get("SENDING_API_TOKEN")}'}
                        request_data = {
                            "id": db_message.id,
                            "phone": client.phone_number,
                            "text": mailing.message_text
                        }

                        async with client_session.post(
                                f"{os.environ.get('SENDING_API_URL')}/send/{db_message.id}",
                                headers=headers, json=request_data) as response:
                            if response.status == 200:
                                send_status = SendStatusEnum.success
                                await logger.create_message_log(
                                    db_message.id,
                                    LoggerLevelsEnum.debug, LoggerActionsEnum.request,
                                    f"[ID:{db_message.id}] Message send success to client ID:{client.id}!"
                                )
                            else:
                                send_status = SendStatusEnum.fail
                                await logger.create_message_log(
                                    db_message.id,
                                    LoggerLevelsEnum.error, LoggerActionsEnum.request,
                                    f"[ID:{db_message.id}] Message send failed to client ID:{client.id}!",
                                    {"error": response.json()}
                                )

                            message_update = MessageUpdate()
                            message_update.send_status = int(send_status)

                            messages_repository.update(db_message, message_update)
                            await messages_repository.commit()

    def start(self):
        self.queue = asyncio.Queue()
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.scheduler.add_job(self.check_mailings, 'interval', seconds=60,
                               # max_instances=1 гарантирует то, что функция не запустится снова,
                               # Если прошлый запуск ещё не окончил свою работу до конца.
                               max_instances=1)
