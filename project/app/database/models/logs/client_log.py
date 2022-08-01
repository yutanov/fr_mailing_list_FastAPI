from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.database.models.logs.log_base import LogBase


class ClientLogBase(LogBase):
    __tablename__ = "logs_clients"


class ClientLog(ClientLogBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created_at: datetime = Field(nullable=False, default=datetime.utcnow())

    client_id: Optional[int] = Field(default=None, foreign_key="clients.id")
    client: Optional["Client"] = Relationship(back_populates="logs")


class ClientLogGet(ClientLogBase):
    id: int

    client_id: Optional[int]
    client: Optional["ClientGet"]


class ClientLogCreate(ClientLogBase):
    client_id: Optional[int]


class ClientLogUpdate(ClientLogBase):
    client_id: Optional[int]


from app.database.models.client import Client, ClientGet

ClientLogGet.update_forward_refs()
