import secrets

from jose.constants import ALGORITHMS

from utlis.common_imports import (
    APIRouter, Depends, HTTPException, OAuth2PasswordRequestForm, OAuth2PasswordBearer, jwt, ExpiredSignatureError, JWTClaimsError, JWTError, os, Annotated, status)
from ServicesDataBases.Service import ServiceData
from datetime import datetime, timedelta

from utlis.funciones_utlis import vefify_salt

router = APIRouter(prefix='/auth', tags=['auth'])
db = ServiceData()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/obtener-token')
es_prod = False
if es_prod:
    secret_value = os.getenv('MY_SECRET_KEY')
else:
    secret_value = 'dev_secret'

SECRET_KEY = "secret_access"
REFRESH_SECRET_KEY = "secret_refresh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

@router.post('/obtener-token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        db.conectar_db()
        user = db.get_one_usuario(form_data.username)

        if not user :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro el usuario')
        psd = vefify_salt(form_data.password, user[0].get('password'))
        if not psd:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Contraseña Incorrecta')

        generar_token = {'username': user[0]['username'], 'email': user[0]['email']}

        access_token = crear_token(
            generar_token,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secret = SECRET_KEY
        )

        refersh_token = crear_token(
            generar_token,
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            secret=REFRESH_SECRET_KEY
        )

        return {'data': {'access_token':access_token, 'expire_acces_token': ACCESS_TOKEN_EXPIRE_MINUTES, 'refersh_token': refersh_token,'expire_refersh_token':REFRESH_TOKEN_EXPIRE_DAYS}}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error Interno {e}")



@router.post('/refresh')
def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token,REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get('username')

        if user is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    generar_token = payload

    new_access_token = crear_token(
        generar_token,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        secret=SECRET_KEY
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


def crear_token(payload: dict, expires_delta: timedelta, secret) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode,secret, algorithm=ALGORITHM)




def decode_token(token: Annotated[str, Depends(oauth2_schema)])-> dict:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        db.conectar_db()
        print(data['username'])
        user = db.get_one_usuario(data['username'])
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