from utlis.common_imports import APIRouter, Depends, HTTPException, JSONResponse, Usuarios,os,status,Annotated
from ServicesDataBases.Service import ServiceData
from routers.auth import decode_token

db = ServiceData()

router = APIRouter(prefix='/usuarios', tags=['usuarios'])

@router.post('/crear')
def crear_usuario(usuario: Usuarios, my_user: Annotated[dict, Depends(decode_token)]):
    try:
        db.conectar_db()
        data = db.create_usuario(usuario=usuario)

        if  data is None:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='EL usuario ya existe')

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)
    except HTTPException as err:
        raise err

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Interno")