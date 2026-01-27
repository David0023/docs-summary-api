from core.config import settings
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy for postgresql
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Class for creating new sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Open a new session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()