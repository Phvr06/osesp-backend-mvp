from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone

class ConcertBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    date: datetime

    @field_validator('date')
    @classmethod
    def validate_date_future(cls, v: datetime) -> datetime:
        if v.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            raise ValueError("A data do concerto deve estar no futuro.")
        return v

class ConcertCreate(ConcertBase):
    pass

class ConcertResponse(ConcertBase):
    id: int
    
    class Config:
        from_attributes = True