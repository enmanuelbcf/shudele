import json

from Model.app_models import Asignatura
from utlis.common_imports import APIRouter, Depends, HTTPException, JSONResponse, University, os,Annotated,status,Annotated
from ServicesDataBases.Service import ServiceData
from routers.auth import decode_token
from utlis.funciones_utlis import convert_time

router = APIRouter(prefix='/universidades', tags=['universidades'])
db = ServiceData()

@router.get("/obtener-universidades")
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

@router.get("/obtener-universidad/{id}")
def obtener_universidad(id: str, my_user: Annotated[dict, Depends(decode_token)]):
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

@router.post('/create_universidad')
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


@router.get("/obtener-universidad-subject/{username}")
def obtener_universidad_subject(username: str):

    try:
        db.conectar_db()
        data = db.get_user_subjects(username)

        day_order = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5, "Sabado": 6, "Domingo": 7}

        for university in data:
            university["subjects"].sort(key=lambda x: (day_order.get(x["day"], 8), convert_time(x["start"])))


        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron datos")

        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
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


@router.post('/registrar_asignatura')
def registrar_asignatura_end(asignatura: Asignatura, my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.registrar_asignatura(asignatura=asignatura)

        if  data is None:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La asignatura ya existe')

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
    except HTTPException as err:
        raise err

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error Interno {e}")