from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str
