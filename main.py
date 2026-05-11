from fastapi import FastAPI
from routers import concert, message, telegram, user

app = FastAPI(title="API", version="1.0.0")

# Acopla as rotas
app.include_router(concert.router)
app.include_router(message.router)
app.include_router(telegram.router)
app.include_router(user.router)
