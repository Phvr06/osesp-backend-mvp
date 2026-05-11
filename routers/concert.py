from fastapi import APIRouter, HTTPException
from typing import List
from schemas.concert import ConcertCreate, ConcertResponse
import mock_db

router = APIRouter(prefix="/concert", tags=["Concertos"])

@router.post("/", response_model=ConcertResponse)
def create_concert(concert: ConcertCreate):
    new_concert = concert.model_dump()
    
    new_concert["id"] = mock_db.concert_id_counter
    mock_db.concert_id_counter += 1
    
    mock_db.concerts_db.append(new_concert)
    return new_concert

@router.get("/", response_model=List[ConcertResponse])
def read_concerts(skip: int = 0, limit: int = 100):
    return mock_db.concerts_db[skip : skip + limit]

@router.get("/{concert_id}", response_model=ConcertResponse)
def read_concert(concert_id: int):
    for c in mock_db.concerts_db:
        if c["id"] == concert_id:
            return c
    raise HTTPException(status_code=404, detail="Concerto não encontrado")

@router.delete("/{concert_id}", response_model=ConcertResponse)
def delete_concert(concert_id: int):
    for i, c in enumerate(mock_db.concerts_db):
        if c["id"] == concert_id:
            deleted_concert = mock_db.concerts_db.pop(i)
            return deleted_concert
    raise HTTPException(status_code=404, detail="Concerto não encontrado")

@router.put("/{concert_id}", response_model=ConcertResponse)
def update_concert(concert_id: int, concert: ConcertCreate):
    for i, c in enumerate(mock_db.concerts_db):
        if c["id"] == concert_id:
            updated_concert = concert.model_dump()
            updated_concert["id"] = concert_id
            mock_db.concerts_db[i] = updated_concert
            return updated_concert
    raise HTTPException(status_code=404, detail="Concerto não encontrado")