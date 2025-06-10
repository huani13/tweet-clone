from fastapi import HTTPException

from .models import TweetModel
from .schemas import TweetCreateSchema, TweetSchema
from ..user import controller as user_controller
from sqlalchemy.orm import Session

from ..tweet.models import TweetModel
from ..follow.models import FollowModel
from ..user.models import UserModel
from ..tweet.schemas import TweetUserSchema

from datetime import datetime

def get_tweet_by_id(tweet_id: int, db: Session):
    tweet = db.query(TweetModel).filter(TweetModel.id == tweet_id).first()
    if not tweet:
        raise HTTPException(
            status_code=404,
            detail=f"Tweet not found"
        )
    return tweet

def create_tweet(tweet: TweetCreateSchema, user_id: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    db_item = TweetModel(**tweet.model_dump())
    db_item.user_id = user_id
    db_item.created_at = db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_tweet(tweet_id: int, updated_tweet: TweetCreateSchema, user_id: int, db: Session):
    tweet = db.query(TweetModel).filter(TweetModel.id == tweet_id).first()
    if not tweet:
        raise HTTPException(
            status_code=404,
            detail=f"Tweet not found"
        )
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    if tweet.user_id != user_id:
        raise HTTPException(
            status_code=400,
            detail=f"User cant update this tweet!"
        )
    tweet.message = updated_tweet.model_dump().get("message")
    tweet.updated_at = datetime.now()
    db.commit()
    db.refresh(tweet)
    return tweet

def delete_tweet(tweet_id: int, user_id: int, db: Session):
    tweet = db.query(TweetModel).filter(TweetModel.id == tweet_id).first()
    if not tweet:
        raise HTTPException(
            status_code=404,
            detail=f"Tweet not found"
        )
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    if tweet.user_id != user_id:
        raise HTTPException(
            status_code=400,
            detail=f"User cant update this tweet!"
        )
    db.delete(tweet)
    db.commit()
    return {"detail": "Delete succesful!"}

def get_tweet_by_user(user_id: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    query_result = db.query(TweetModel, UserModel).filter(
        TweetModel.user_id == user_id
    ).filter(
        TweetModel.user_id == UserModel.id
    ).order_by(TweetModel.created_at.desc())
    result = []
    for tweet, user in query_result:
        entry = TweetUserSchema()
        entry.tweet_id = tweet.id
        entry.tweet_message = tweet.message
        entry.tweet_created_at = tweet.created_at
        entry.tweete_updated_at = tweet.updated_at
        entry.user_id = user.id
        entry.user_name = user.name
        result.append(entry)

    return result