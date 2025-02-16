import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from jose import jwt, ExpiredSignatureError
from jose.exceptions import JWTClaimsError, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ServicesDataBases.Service import ServiceData
from Model.app_models import University, Usuarios