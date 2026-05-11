from fastapi import APIRouter, HTTPException
from typing import List
from schemas.user import UserCreate, UserResponse
import mock_db

router = APIRouter(prefix="/user", tags=["Usuários"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    for existing_user in mock_db.users_db:
        if existing_user["phone"] == user.phone:
            raise HTTPException(status_code=400, detail="Telefone já cadastrado")
    
    new_user = user.model_dump()
    new_user["id"] = mock_db.user_id_counter
    mock_db.user_id_counter += 1
    
    mock_db.users_db.append(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100):
    return mock_db.users_db[skip : skip + limit]

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    for u in mock_db.users_db:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int):
    for i, u in enumerate(mock_db.users_db):
        if u["id"] == user_id:
            deleted_user = mock_db.users_db.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    for i, u in enumerate(mock_db.users_db):
        if u["id"] == user_id:
            updated_user = user.model_dump()
            updated_user["id"] = user_id
            mock_db.users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")