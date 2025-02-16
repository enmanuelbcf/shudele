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



@router.post('/obtener-token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db.conectar_db()
    user = db.get_one_usuario(form_data.username)
    psd = vefify_salt(form_data.password, user[0].get('password'))
    if not user or not psd :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No se encontro el usuario')
    token = encode_token({'username': user[0]['username'], 'email': user[0]['email']})
    return {'access_token': token,
            'exp': 3600
            }

def encode_token(payload: dict) -> str:
    expiration = datetime.utcnow() + timedelta(seconds=3600)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, secret_value, algorithm='HS256')
    return token

def encode_refres_token(payload: dict) -> str:
    expiration = datetime.utcnow() + timedelta(days=1)
    payload.update({"exp": expiration})
    token = jwt.encode(payload, secret_value, algorithm='HS256')
    return token


def decode_token(token: Annotated[str, Depends(oauth2_schema)])-> dict:
    try:
        data = jwt.decode(token, secret_value, algorithms=['HS256'])
        # user = .get(data['username'])
        db.conectar_db()
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