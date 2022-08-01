from fastapi import FastAPI

from .api import router as api_router
from .scheduler import SchedulerService


tags_metadata = [
    {
        "name": "Logs",
        "description": "Получение логов",
    },
    {
        "name": "Clients",
        "description": "Редактирование клиентов"
    },
    {
        "name": "Mailings",
        "description": "Редактирование рассылок"
    },
    {
        "name": "Messages",
        "description": "Просмотр отправленных сообщений"
    }
]

description = """
API для администрирования рассылками.

## Clients
#### Управление клиентами

* `[GET]` **/clients** - Получает всех клиентов.
* `[GET]` **/clients/{id}** - Получает клиента по ID.
* `[POST]` **/clients** - Добавляет клиента.
* `[UPDATE]` **/clients/{id}** - Обновляет клиента по ID.
* `[DELETE]` **/clients/{id}** - Удаляет клиента по ID.


## Mailings
#### Управление Рассылкой

* `[GET]` **/mailings** - Получает все рассылки.
* `[GET]` **/mailings/{id}** - Получает рассылку по ID.
* `[POST]` **/mailings** - Добавляет рассылку.
* `[UPDATE]` **/mailings/{id}** - Обновляет рассылку по ID.
* `[DELETE]` **/mailings/{id}** - Удаляет рассылку по ID.
  
  
## Messages
#### Управление Сообщениями

* `[GET]` **/mailings** - Получает все сообщения.
* `[GET]` **/mailings/{id}** - Получает сообщение по ID.
* `[DELETE]` **/mailings/{id}** - Удаляет сообщение по ID.
  
  
## Logs
#### Просмотр логов

* `[GET]` **/logs/clients** - Получает все логи операций с клиентами
* `[GET]` **/logs/clients/{id}** - Получает все логи операций с клиентом по ID клиента
* `[GET]` **/logs/mailings** - Получает все логи операций с рассылками
* `[GET]` **/logs/mailings/{id}** - Получает все логи операций с рассылкой по ID рассылки
* `[GET]` **/logs/messages** - Получает все логи операций с сообщениями
* `[GET]` **/logs/messages/{id}** - Получает все логи операций с сообщением по ID сообщения
"""

app = FastAPI(
    title="MailingAPI",
    openapi_tags=tags_metadata,
    description=description,
    version="0.0.1",
)
app.include_router(api_router)

# Запускаем фоновый процесс, который проверяет и отправляет уведомления.
scheduler = SchedulerService()
scheduler.start()
