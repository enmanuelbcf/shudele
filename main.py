import sqlite3
from datetime import datetime, timedelta
from logging import raiseExceptions
from wsgiref.util import request_uri

import uvicorn
from fastapi import FastAPI, HTTPException, status, Form
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt, ExpiredSignatureError
from pydantic import BaseModel, ValidationError
from sniffio import AsyncLibraryNotFoundError
from starlette.status import HTTP_400_BAD_REQUEST


# Conectar a la base de datos
import sqlite3


def conectar_db():
    try:
        con = sqlite3.connect('./DataBases/db')
        con.row_factory = sqlite3.Row  # Permite obtener los resultados como diccionarios
        return con
    except sqlite3.Error as e:
        print(f'Error al conectar: {e}')
        return None

# Obtener todas las universidades y devolver un objeto JSON clave-valor
def get_all():
    con = conectar_db()
    if con is None:
        return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Universidad")
        rows = cursor.fetchall()
        con.close()  # Cerrar conexión

        if rows:
            data = [dict(row) for row in rows]  # Convertir cada fila en un diccionario clave-valor
            return data
        else:
            return None

    except sqlite3.Error as e:
        print(f'Error en la consulta: {e}')
        return None

def get_one(id):
    con = conectar_db()
    if con is None:
        return {"status": "error", "message": "Error al conectar a la base de datos", "data": []}

    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Universidad where universidad_id = ? ",[id] )
        rows = cursor.fetchall()
        con.close()  # Cerrar conexión

        if rows:
            data = [dict(row) for row in rows]  # Convertir cada fila en un diccionario clave-valor
            return data
        else:
            return None

    except sqlite3.Error as e:
        print(f'Error en la consulta: {e}')
        return None

app = FastAPI()
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
        data = get_all()

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
def obtener_universid(id: int, my_user: Annotated[dict, Depends(decode_token)]):  # Protegido con token
    try:
        data = get_one(id)

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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
