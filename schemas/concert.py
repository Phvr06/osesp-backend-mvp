from pydantic import BaseModel, Field
from datetime import datetime

class ConcertBase(BaseModel):
    id_site: int = Field(..., description="ID do programa no site da OSESP")
    nome: str = Field(..., min_length=3, max_length=150)
    data: datetime
    local: str = Field(default="Sala São Paulo", min_length=3)

class ConcertCreate(ConcertBase):
    pass

class ConcertResponse(ConcertBase):
    id: int
    
    class Config:
        from_attributes = True