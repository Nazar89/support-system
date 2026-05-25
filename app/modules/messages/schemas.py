from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str


class MessageRead(BaseModel):
    id: int
    ticket_id: int
    sender_id: int
    text: str

    class Config:
        from_attributes = True
