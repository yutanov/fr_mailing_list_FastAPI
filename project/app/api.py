from fastapi import APIRouter
from app.endpoints import clients, logs, mailings, messages

router = APIRouter()
router.include_router(clients.router)
router.include_router(mailings.router)
router.include_router(messages.router)
router.include_router(logs.router)
