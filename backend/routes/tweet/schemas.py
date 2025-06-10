from pydantic import BaseModel


class TweetSchema(BaseModel):
    id: int | None = None
    user_id: int
    message: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class TweetCreateSchema(BaseModel):
    message: str

    class Config:
        orm_mode = True

class TweetUserSchema():
    tweet_id: int
    tweet_message: str
    tweet_created_at: str
    tweete_updated_at: str
    user_id: int
    user_name: str