from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from routes.tweet import controller

from typing import Annotated

from fastapi import Header

from config.db_dependency import get_db
from .controller import *
from .schemas import *

router = APIRouter(
    prefix="/tweet",
    tags=["Tweet"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.get("/{tweet_id}")
async def get_tweet(tweet_id, db: Session = Depends(get_db)):
    return get_tweet_by_id(tweet_id, db=db)

@router.post("/")
async def create_tweet(tweet: TweetCreateSchema, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.create_tweet(tweet, user_id, db)

@router.put("/{tweet_id}")
async def update_tweet(tweet_id: int, tweet: TweetCreateSchema, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.update_tweet(tweet_id, tweet, user_id, db)

@router.delete("/{tweet_id}")
async def delete_tweet(tweet_id: int, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.delete_tweet(tweet_id, user_id, db)

@router.get("/user/{user_id}")
async def get_tweet_by_user(user_id: int, db: Session = Depends(get_db)):
    return controller.get_tweet_by_user(user_id, db)