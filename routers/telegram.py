import json
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas.telegram

router = APIRouter(prefix="/telegram", tags=["Telegram"])

@router.post("/send", response_model=schemas.telegram.TelegramResponse)
def send_telegram_message(payload: schemas.telegram.TelegramMessageCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == payload.usuario_id).first()
    template = db.query(models.TemplateDB).filter(models.TemplateDB.id == payload.template_id).first()
    
    if not usuario or not template:
        raise HTTPException(status_code=404, detail="Dados insuficientes no banco")
        
    concerto = template.concerto

    iso_date_url = concerto.data.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    readable_date = concerto.data.strftime('%d/%m/%Y - %Hh%M')

    db_mensagem = models.MensagemDB(
        usuario_id=payload.usuario_id,
        template_id=payload.template_id,
        data_envio=datetime.now(),
        provider="telegram",
        status="enviando"
    )
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)

    bot_payload = {
        "user_id": str(usuario.contato),
        "eventUrl": f"https://osesp.art.br/osesp/pt/concerto/{concerto.id_oficial}?date={iso_date_url}",
        "message": template.conteudo,
        "date": readable_date,
        "location": concerto.local,
        "hasConfirmation": payload.has_confirmation
    }

    body = json.dumps(bot_payload).encode("utf-8")
    request = Request(
        str(payload.bot_notify_url),
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            db_mensagem.status = "enviado"
            db.commit()
            return {
                "detail": "Notificação enviada ao bot",
                "telegram_api_code": response.getcode(),
                "mensagem_id": db_mensagem.id
            }
    except HTTPError as exc:
        db_mensagem.status = f"erro_{exc.code}"
        db.commit()
        raise HTTPException(status_code=exc.code, detail="Falha na integração com o bot")
    except Exception as e:
        db_mensagem.status = "erro_desconhecido"
        db.commit()
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/webhook-receiver")
def receive_reply(callback: schemas.telegram.TelegramCallbackPayload, db: Session = Depends(get_db)):
    """
    Endpoint configurado como CALLBACK_URL no bot.
    Recebe a resposta do usuário e atualiza a auditoria.
    """
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.contato == callback.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não identificado")

    msg_original = (
        db.query(models.MensagemDB)
        .join(models.TemplateDB)
        .filter(
            models.MensagemDB.usuario_id == usuario.id,
            models.TemplateDB.concerto_id == callback.eventId
        )
        .order_by(models.MensagemDB.data_envio.desc())
        .first()
    )

    if msg_original:
        nova_resposta = models.RespostaDB(
            mensagem_id=msg_original.id,
            resposta="Confirmado" if callback.confirmed else "Cancelado",
            timestamp=datetime.now()
        )
        db.add(nova_resposta)
        
        if not callback.confirmed:
            msg_original.status = "devolucao_solicitada"
            
        db.commit()
    
    return {"status": "ok"}