from fastapi import HTTPException

from .models import FollowModel
from .schemas import FollowCreateSchema, FollowSchema
from ..user import controller as user_controller
from sqlalchemy.orm import Session

from datetime import datetime

def get_follower_of_user_id(user_id: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    return db.query(FollowModel).filter(
        FollowModel.following_id == user_id).all()

def get_following_of_user_id(user_id: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    return db.query(FollowModel).filter(
        FollowModel.follower_id == user_id).all()

def create_follow(user_id: int, following_id: int, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    if following_id is None or not user_controller.is_user_id_exist(following_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    if following_id == user_id:
        raise HTTPException(
            status_code=400,
            detail=f"Bad request"
        )
    follow_item = get_follow_item(user_id, following_id, db)
    if (follow_item != None):
        raise HTTPException(
            status_code=400,
            detail=f"User is currently following!"
        )
    db_item = FollowModel()
    db_item.follower_id = user_id
    db_item.following_id = following_id
    db_item.created_at = datetime.now()
    db.add(db_item)
    db.commit()
    return {"detail": "Successfully followed!"}

def delete_follow(user_id: int, following_id, db: Session):
    if user_id is None or not user_controller.is_user_id_exist(user_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    if following_id is None or not user_controller.is_user_id_exist(following_id, db):
        raise HTTPException(
            status_code=400,
            detail=f"User Id not exist!"
        )
    follow_item = get_follow_item(user_id, following_id, db)
    if (follow_item == None):
        raise HTTPException(
            status_code=400,
            detail=f"User is not currently following!"
        )
    db.delete(follow_item)
    db.commit()
    return {"detail": "Successfully unfollowed!"}

def get_follow_item(follower_id: int, following_id: int, db: Session):
    return db.query(FollowModel).filter(
        FollowModel.follower_id == follower_id).filter(
        FollowModel.following_id == following_id
        ).first()