import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter(prefix="/telegram", tags=["Telegram"])


class TelegramMessage(BaseModel):
    webhook_url: HttpUrl
    message: str = Field(..., min_length=1, max_length=4096)


@router.post("/send")
def send_telegram_message(payload: TelegramMessage):
    body = json.dumps({"text": payload.message}).encode("utf-8")
    request = Request(
        str(payload.webhook_url),
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8") or exc.reason
        raise HTTPException(status_code=exc.code, detail=detail) from exc
    except URLError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao enviar mensagem para o Telegram: {exc.reason}",
        ) from exc

    return {
        "detail": "Mensagem enviada para o Telegram",
        "telegram_response": response_body,
    }
