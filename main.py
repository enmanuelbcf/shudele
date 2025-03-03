import asyncio
import uvicorn
from fastapi import FastAPI
from routers import usuario, universidades, auth, push_notification
from routers.push_notification import send_push
from contextlib import asynccontextmanager

app = FastAPI()

# Usamos el decorador asynccontextmanager para manejar el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Llamamos a send_push al iniciar
    asyncio.create_task(send_push())
    yield
    # Aquí puedes manejar la limpieza cuando la aplicación termine
    print("Cerrando la aplicación...")

app = FastAPI(lifespan=lifespan)

# Incluir routers
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(universidades.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
