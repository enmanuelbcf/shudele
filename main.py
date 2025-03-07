import asyncio
from datetime import datetime
from os import utime

import pytz
import uvicorn
from fastapi import FastAPI
from routers import usuario, universidades, auth, utils
from routers.push_notification import schedule

app = FastAPI()

schedule()
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(universidades.router)
app.include_router(utils.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
