from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from database import get_db
import models

router = APIRouter(prefix="/user", tags=["Usuários"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.UsuarioDB).filter(models.UsuarioDB.contato == user.contato).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Contato já cadastrado")
    
    new_user = models.UsuarioDB(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.UsuarioDB).offset(skip).limit(limit).all()

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    for key, value in user_data.model_dump().items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    return user