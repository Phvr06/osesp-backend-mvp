from pydantic import BaseModel, Field

class UserBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    contato: str = Field(..., description="Telefone ou Email válido")
    tipo: str = Field(..., description="Ex: assinante, avulso, cortesia")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True