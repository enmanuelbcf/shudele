from Model.app_models import UsuariosCreate
from utlis.common_imports import APIRouter, Depends, HTTPException, JSONResponse, Usuarios,os,status,Annotated
from ServicesDataBases.Service import ServiceData
from routers.auth import decode_token

db = ServiceData()

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

@router.post('/crear')
def crear_usuario(usuario: UsuariosCreate):
    try:
        db.conectar_db()
        data = db.create_usuario(usuario=usuario)

        if  data is None:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='EL usuario ya existe')

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
    except HTTPException as err:
        raise err

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Interno")

@router.get("/obtener-usuarios")
def obtener_usuarios(my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.get_all_usuario()

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

@router.get("/obtener-usuario/{id}")
def obtener_usuarios(id: str, my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.get_one_usuario(id)

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