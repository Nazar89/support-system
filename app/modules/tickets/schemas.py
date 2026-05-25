from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str


class TicketRead(BaseModel):
    id: int
    title: str
    description: str
    status: str
    owner_id: int

    class Config:
        from_attributes = True


class TicketStatusUpdate(BaseModel):
    status: str
