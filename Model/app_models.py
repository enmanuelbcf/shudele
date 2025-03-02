import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field,EmailStr
from passlib.context import CryptContext


class Enum_estados(str, Enum):
    activo = 'AC'
    inactivo = 'ÍN'


class University(BaseModel):
    universidad_id: str
    nombre_universidad: str = Field(max_length=50)
    acronimo_universidad: str = Field(max_length=8)
    foto: Optional[str]

class Usuarios(BaseModel):
    usuario_id: str
    username: str = Field(max_length=20)
    email: EmailStr
    password: str = Field(min_length=1)

class Asignatura(BaseModel):
    asignatura_id: str
    nombre: str = Field(max_length=100)
    dia: str
    hora_inicio: str
    hora_fin: str
    aula: str
    universidad_id: str
    username: str

    