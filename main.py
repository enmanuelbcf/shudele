import asyncio
import uvicorn
from fastapi import FastAPI
from routers import usuario, universidades, auth, push_notification
from routers.push_notification import send_push

app = FastAPI()
send_push()
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(universidades.router)
asyncio.run(send_push())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


