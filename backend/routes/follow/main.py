from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from routes.follow import controller

from typing import Annotated

from fastapi import Header

from config.db_dependency import get_db
from .controller import *
from .schemas import *

router = APIRouter(
    prefix="/follow",
    tags=["Follow"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.get("/follower")
async def get_follower(db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return get_follower_of_user_id(user_id, db=db)

@router.get("/following")
async def get_following(db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return get_following_of_user_id(user_id, db=db)

@router.post("/follow/{following_id}")
async def create_follow(following_id: int, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.create_follow(user_id, following_id, db)

@router.delete("/follow/{following_id}")
async def delete_follow(following_id: int, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.delete_follow(user_id, following_id, db)
