import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from jose.exceptions import JWTClaimsError, JWTError
from starlette import status
from ServicesDataBases.Service import ServiceData


