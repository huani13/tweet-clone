from config.database import Base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=30))
    created_at = Column(DateTime, default=datetime.now())