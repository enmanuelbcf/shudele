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
    username: str = Field(max_length=10)
    email: EmailStr
    password: str = Field(max_length=8, min_length=1)

    # Función para encriptar la contraseña

    