from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

class TweetModel(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    message = Column(String(length=300))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())