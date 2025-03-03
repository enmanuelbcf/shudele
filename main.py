import asyncio
from datetime import datetime

import pytz
import uvicorn
from fastapi import FastAPI
from routers import usuario, universidades, auth
from routers.push_notification import send_push
from contextlib import asynccontextmanager

app = FastAPI()
zona_horaria = pytz.timezone('America/Santo_Domingo')  # Zona horaria de RD, que es UTC -4

# Obtener la hora actual en la zona horaria de UTC -4
ahora = datetime.now(zona_horaria)
hora_actual = ahora.time()
send_push()
print(hora_actual)
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(universidades.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
