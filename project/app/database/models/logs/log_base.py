from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel

from app.utils.models_utils import enum_elements_to_string


class LoggerLevelsEnum(IntEnum):
    debug = 0
    info = 1
    error = 2
    warning = 3


class LoggerActionsEnum(IntEnum):
    create = 1
    update = 2
    delete = 3
    request = 4


class LogBase(SQLModel):
    level: int = Field(
        nullable=False,
        title="Уровень лога", description=f"Доступные значения:\n"
                                          f"{enum_elements_to_string(LoggerLevelsEnum)}"
    )
    action: int = Field(
        nullable=False,
        title="Тип действия", description=f"Доступные значения:\n"
                                          f"{enum_elements_to_string(LoggerActionsEnum)}"
    )
    message_text: str = Field(
        nullable=False, default="No Message",
        title="Текст лога"
    )
    data_json: str = Field(
        nullable=False, default="{\"error\": \"Example Text\"}",
        title="Json строка с дополнительными данными к логу"
    )


class LogUpdateBase(SQLModel):
    level: Optional[int]
    action: Optional[int]
    message_text: Optional[str]
    data_json: Optional[str]
