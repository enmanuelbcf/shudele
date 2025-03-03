import uuid
from enum import Enum
from typing import Optional, Union, List
from pydantic import BaseModel, Field,EmailStr
from passlib.context import CryptContext


class Enum_estados(str, Enum):
    activo = 'AC'
    inactivo = 'ÍN'


class University(BaseModel):
    universidad_id: int
    nombre_universidad: str = Field(max_length=50)
    acronimo_universidad: str = Field(max_length=8)
    foto: Optional[str]

class Usuarios(BaseModel):
    usuario_id: str
    username: str = Field(max_length=20)
    email: EmailStr
    password: str = Field(min_length=1)

class Asignatura(BaseModel):
    nombre: str = Field(max_length=100)
    dia: str
    hora_inicio: str
    hora_fin: str
    aula: str
    universidad_id: int
    username: str

class AsignaturaDTO(BaseModel):
    asignatura_id: Optional[int]
    nombre: str = Field(max_length=100)
    dia: str
    hora_inicio: str
    hora_fin: str
    aula: str
    universidad_id: int
    username: str

class Notificacion(BaseModel):
    horas: List[str]
    asignatura: str
    universidad: str
