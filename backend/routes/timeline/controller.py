from fastapi import HTTPException

from ..tweet.models import TweetModel
from ..follow.models import FollowModel
from ..user.models import UserModel
from ..tweet.schemas import TweetUserSchema
# from .schemas import TweetCreateSchema, TweetSchema
from ..user import controller as user_controller
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from datetime import datetime

def get_timeline(user_id: int, offset: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    limit = 15
    followed_user_dto = db.query(FollowModel).filter(FollowModel.follower_id == user_id).all()
    include_tweet_user_ids = [user_id]
    for user_dto in followed_user_dto:
        include_tweet_user_ids.append(user_dto.following_id)
    query_result = db.query(TweetModel, UserModel).filter(
        TweetModel.user_id == UserModel.id
    ).filter(
        TweetModel.user_id.in_(include_tweet_user_ids)
    ).order_by(TweetModel.created_at.desc()
    ).offset(offset).limit(limit).all()
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