from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None = None
    name: str
    created_at: str

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True