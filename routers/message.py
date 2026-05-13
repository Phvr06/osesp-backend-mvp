from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas.message import MessageCreate, MessageResponse
from database import get_db
import models

router = APIRouter(prefix="/message", tags=["Mensagens"])

def _user_exists(user_id: int, db: Session) -> bool:
    return db.query(models.UsuarioDB).filter(models.UsuarioDB.id == user_id).first() is not None

def _template_exists(template_id: int, db: Session) -> bool:
    return db.query(models.TemplateDB).filter(models.TemplateDB.id == template_id).first() is not None

@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    if not _user_exists(message.usuario_id, db):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not _template_exists(message.template_id, db):
        raise HTTPException(status_code=404, detail="Template não encontrado")

    new_message = models.MensagemDB(**message.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/", response_model=List[MessageResponse])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.MensagemDB).offset(skip).limit(limit).all()

@router.get("/{message_id}", response_model=MessageResponse)
def read_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.MensagemDB).filter(models.MensagemDB.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return message