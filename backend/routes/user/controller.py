from fastapi import HTTPException
from pydantic import EmailStr

from .models import UserModel
from .schemas import UserCreateSchema, UserSchema
from sqlalchemy.orm import Session

from datetime import datetime


def get_users(db: Session):
    users = db.query(UserModel).all()
    return users

def is_name_exist(name: str, db:Session):
    count = db.query(UserModel).filter(UserModel.name == name).count()
    return count > 0

def is_user_id_exist(user_id: int, db:Session):
    count = db.query(UserModel).filter(UserModel.id == user_id).count()
    return count > 0

def create_user(user: UserCreateSchema, db: Session):
    if is_name_exist(user.name, db):
        raise HTTPException(
            status_code=400,
            detail=f"Username already exist: {user.name}"
        )
    db_item = UserModel(**user.model_dump())
    db_item.created_at = datetime.now()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def search_user(search_key: str, db: Session):
    if len(search_key) < 3:
        raise HTTPException(
            status_code=400,
            detail=f"Search key too short!"
        )
    return db.query(UserModel).filter(UserModel.name.ilike(f'%{search_key}%')).all()