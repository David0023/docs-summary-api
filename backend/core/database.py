from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# SQLAlchemy for postgresql
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Class for creating new sessions
SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)

# Base class for all models
Base = declarative_base()

