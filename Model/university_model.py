import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class Enum_estados(str, Enum):
    activo = 'AC'
    inactivo = 'ÍN'


class University(BaseModel):
    universidad_id: str
    nombre_universidad: str = Field(max_length=50)
    acronimo_universidad: str = Field(max_length=8)
    foto: Optional[str]