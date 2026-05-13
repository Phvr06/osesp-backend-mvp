from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas.concert import ConcertCreate, ConcertResponse
from database import get_db
import models

router = APIRouter(prefix="/concert", tags=["Concertos"])

@router.post("/", response_model=ConcertResponse)
def create_concert(concert: ConcertCreate, db: Session = Depends(get_db)):
    db_concert = models.ConcertoDB(**concert.model_dump())
    db.add(db_concert)
    db.commit()
    db.refresh(db_concert)
    return db_concert

@router.get("/", response_model=List[ConcertResponse])
def read_concerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ConcertoDB).offset(skip).limit(limit).all()

@router.get("/{concert_id}", response_model=ConcertResponse)
def read_concert(concert_id: int, db: Session = Depends(get_db)):
    concert = db.query(models.ConcertoDB).filter(models.ConcertoDB.id == concert_id).first()
    if not concert:
        raise HTTPException(status_code=404, detail="Concerto não encontrado")
    return concert

@router.delete("/{concert_id}", response_model=ConcertResponse)
def delete_concert(concert_id: int, db: Session = Depends(get_db)):
    concert = db.query(models.ConcertoDB).filter(models.ConcertoDB.id == concert_id).first()
    if not concert:
        raise HTTPException(status_code=404, detail="Concerto não encontrado")
    
    db.delete(concert)
    db.commit()
    return concert

@router.put("/{concert_id}", response_model=ConcertResponse)
def update_concert(concert_id: int, concert_data: ConcertCreate, db: Session = Depends(get_db)):
    concert = db.query(models.ConcertoDB).filter(models.ConcertoDB.id == concert_id).first()
    if not concert:
        raise HTTPException(status_code=404, detail="Concerto não encontrado")
    
    for key, value in concert_data.model_dump().items():
        setattr(concert, key, value)
        
    db.commit()
    db.refresh(concert)
    return concert