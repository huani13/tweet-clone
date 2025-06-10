from pydantic import BaseModel

class FollowSchema(BaseModel):
    follower_id: int
    following_id: int
    created_at: str

    class Config:
        orm_mode = True

class FollowCreateSchema(BaseModel):
    followingId: int

    class Config:
        orm_mode = True