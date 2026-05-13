from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class TelegramMessageCreate(BaseModel):
    usuario_id: int
    template_id: int
    bot_notify_url: HttpUrl = Field(..., description="URL do bot (ex: http://localhost:3000/notify)")
    has_confirmation: int = 1

class TelegramCallbackPayload(BaseModel):
    user_id: str
    eventId: str
    confirmed: bool

class TelegramResponse(BaseModel):
    detail: str
    telegram_api_code: int
    mensagem_id: int