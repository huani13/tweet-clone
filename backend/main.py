from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

from routes import user
from routes.user import main, models

from routes import tweet
from routes.tweet import main, models

from routes import follow
from routes.follow import main, models

from routes import timeline
from routes.timeline import main

from config.database import engine

user.models.Base.metadata.create_all(bind=engine)
tweet.models.Base.metadata.create_all(bind=engine)
follow.models.Base.metadata.create_all(bind=engine)

# ----------------------------------------

# FastAPI app instance
app = FastAPI()

app.include_router(user.main.router)
app.include_router(tweet.main.router)
app.include_router(follow.main.router)
app.include_router(timeline.main.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)