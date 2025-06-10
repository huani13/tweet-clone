from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from routes.user import controller

from typing import Annotated
from config.db_dependency import get_db
from .controller import *
from .schemas import *

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return get_users(db=db)

@router.post("/")
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    return controller.create_user(user, db)

@router.get("/search")
async def search_user(search_key: Annotated[str | None, Query(max_length=50)] = None, db: Session = Depends(get_db)):
    return controller.search_user(search_key, db)