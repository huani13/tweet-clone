from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from routes.timeline import controller

from typing import Annotated

from fastapi import Header, Query

from config.db_dependency import get_db
from .controller import *

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.get("/")
async def get_timeline(offset: Annotated[int | None, Query()] = 0, db: Session = Depends(get_db), user_id: Annotated[int | None, Header()] = None):
    return controller.get_timeline(user_id, offset, db)