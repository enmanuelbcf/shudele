import os.path
import sqlite3
from datetime import datetime, timedelta
from http.client import responses, HTTPResponse
from logging import raiseExceptions
from wsgiref.util import request_uri

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError
from starlette.responses import JSONResponse
import json

from Model.university_model import  University, Enum_estados
import uuid
from pydantic import BaseModel, ValidationError
from sniffio import AsyncLibraryNotFoundError
from starlette.status import HTTP_400_BAD_REQUEST

from ServicesDataBases.Service import *

# Conectar a la base de datos


app = FastAPI()

PATH = os.path.abspath('DataBases/db')

db = ServiceData(con=PATH)




oauth2_schema = OAuth2PasswordBearer(tokenUrl='obtener-token')

def encode_token(payload: dict) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, 'my-secret', algorithm='HS256')
    return token

def decode_token(token: Annotated[str, Depends(oauth2_schema)])-> dict:
    try:
        data = jwt.decode(token, 'my-secret', algorithms=['HS256'])
        user = users.get(data['username'])
        return user
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Endpoint protegido por token'
        )
    except JWTClaimsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Endpoint protegido por token'
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Token Invalido'
        )


users = {
    'enmanuelbcf':{
        'username':'Enmanuel',
        'email': 'enmanuelbcf@gmail.com',
        'password': 'Prueba01*'
    }
}
@app.post('/obtener-token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or users.get('enmanuelbcf')['password'] != form_data.password :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro el usuario')
    token = encode_token({'username': user['username'], 'email': user['email']})
    return {'access_token': token,
            'exp': 30
            }

@app.get("/universidad/obtener-universidades")
def obtener_universidades(my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.get_all_universidades()

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos")


        return {"status": "success", "data":data}

    except HTTPException as err:
        if err.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Endpoint protegido por token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise err
    except Exception as a:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error Interno')

@app.get("/universidad/obtener-universidad/{id}")
def obtener_universidad(id: str, my_user: Annotated[dict, Depends(decode_token)]):  # Protegido con token
    try:
        db.conectar_db()
        data = db.get_one_universidad(id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos")

        return {"status": "success", "data": data}

    except HTTPException as err:
        if err.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Endpoint protegido por token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise err
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Interno")

@app.post('/universidad/create_universidad')
def crear_universidad(universidad: University, my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.create_universidad(universidad=universidad)

        if  data is None:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='EL usuario ya existe')

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
    except HTTPException as err:
        raise err

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Interno")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
