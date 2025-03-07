from utlis.common_imports import APIRouter, Depends, HTTPException, JSONResponse, Usuarios,os,status,Annotated

from ServicesDataBases.Service import ServiceData



router = APIRouter(prefix='/utils', tags=['utils'])





@router.get('/obtener-historico')
def historico():
    try:
        db = ServiceData()
        db.conectar_db()
        data = db.get_historico()

        if data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No hay historico')

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Interno")


