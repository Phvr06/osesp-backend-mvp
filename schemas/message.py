from pydantic import BaseModel, Field
from datetime import datetime

class MessageBase(BaseModel):
    usuario_id: int
    template_id: int
    data_envio: datetime
    provider: str = Field(..., description="Ex: wpp, telegram")
    status: str = Field(default="pendente")

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    
    class Config:
        from_attributes = True