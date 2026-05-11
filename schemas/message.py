from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    user_id: int | None = None
    concert_id: int | None = None


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int

    class Config:
        from_attributes = True
