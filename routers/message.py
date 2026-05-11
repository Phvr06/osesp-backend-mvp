from typing import List
from fastapi import APIRouter, HTTPException
from schemas.message import MessageCreate, MessageResponse
import mock_db

router = APIRouter(prefix="/message", tags=["Mensagens"])


def _user_exists(user_id: int) -> bool:
    return any(user["id"] == user_id for user in mock_db.users_db)


def _concert_exists(concert_id: int) -> bool:
    return any(concert["id"] == concert_id for concert in mock_db.concerts_db)


@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate):
    if message.user_id is not None and not _user_exists(message.user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if message.concert_id is not None and not _concert_exists(message.concert_id):
        raise HTTPException(status_code=404, detail="Concerto não encontrado")

    new_message = message.model_dump()
    new_message["id"] = mock_db.message_id_counter
    mock_db.message_id_counter += 1

    mock_db.messages_db.append(new_message)
    return new_message


@router.get("/", response_model=List[MessageResponse])
def read_messages(skip: int = 0, limit: int = 100):
    return mock_db.messages_db[skip : skip + limit]


@router.get("/{message_id}", response_model=MessageResponse)
def read_message(message_id: int):
    for message in mock_db.messages_db:
        if message["id"] == message_id:
            return message
    raise HTTPException(status_code=404, detail="Mensagem não encontrada")
