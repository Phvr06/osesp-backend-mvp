from fastapi import FastAPI
from database import engine, Base
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import concert, user, message, telegram, template

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SHOW UP - API OSESP", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(concert.router)
app.include_router(user.router)
app.include_router(template.router)
app.include_router(message.router)
app.include_router(telegram.router)