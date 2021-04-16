from sqlalchemy import Column, String, Integer

from .database import Base

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)