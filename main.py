import sqlite3
from logging import raiseExceptions

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_400_BAD_REQUEST


# Conectar a la base de datos
import sqlite3

# Conectar a la base de datos
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

@app.get("/universidad/obtener-universidades")
def obtener_universidades():
    try:
        data = get_all()

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos")

        return {"status": "success", "data":data}

    except HTTPException as err:
        raise err
    except Exception as a:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error Interno')

@app.get("/universidad/obtener-universidad/{id}")
def obtener_universid(id:int):
    try:
        data = get_one(id)

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos")

        return {"status": "success", "data":data}

    except HTTPException as err:
        raise err
    except Exception as a:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error Interno')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
