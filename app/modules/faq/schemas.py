from pydantic import BaseModel


class FAQCreate(BaseModel):
    question: str
    answer: str


class FAQRead(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True
