from pydantic import BaseModel, Field

class TemplateBase(BaseModel):
    concerto_id: int = Field(..., description="ID da sessão do concerto no banco de dados")
    tipo: str = Field(..., description="Ex: T-7, T-48, T-4")
    conteudo: str = Field(..., description="Texto do lembrete")

class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    id: int
    
    class Config:
        from_attributes = True