from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import User

async def get_one_user(db: AsyncSession, **kwargs) -> User | None:
    query = select(User).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_many_users(db: AsyncSession, **kwargs) -> List[User]:
    query = select(User).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalars().all()

async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str) -> User:
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
