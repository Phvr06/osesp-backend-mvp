from pydantic import BaseModel, Field, field_validator
import re

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    phone: str = Field(..., description="Telefone com DDD (11 a 99) + 9 + 8 dígitos")
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = re.sub(r'\D', '', v)
    
        if not re.match(r"^[1-9]{2}9\d{8}$", v):
            raise ValueError("Telefone inválido.")
        
        return v

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True