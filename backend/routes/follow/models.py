from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime, PrimaryKeyConstraint, Index
from datetime import datetime

class FollowModel(Base):
    __tablename__ = 'follow'

    follower_id = Column(Integer, primary_key=True)
    following_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    Index('following_idx', 'following_id', 'follower_id')