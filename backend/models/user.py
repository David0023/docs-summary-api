from sqlalchemy import Column, Integer, String
from models.base import BaseModel, TimestampMixin

class User(BaseModel, TimestampMixin):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)