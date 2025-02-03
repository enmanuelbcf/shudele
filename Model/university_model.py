from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Enum_estados(str, Enum):
    activo = 'AC'
    inactivo = 'ÍN'


class University(BaseModel):
    universidad_id: int
    nombre_universidad: str = Field(max_length=50)
    acronimo_universidad: str = Field(max_length=8)
    foto: Optional[str]