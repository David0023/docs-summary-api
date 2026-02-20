from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.job import Job
from core.enums import JobStatus

async def get_one_job(db: AsyncSession, **kwargs) -> Job | None:
    query = select(Job).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_many_jobs(db: AsyncSession, **kwargs) -> List[Job]:
    query = select(Job).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalars().all()

async def create_job(db: AsyncSession, user_id: int, title: str, description: str) -> Job:
    new_job = Job(
        user_id=user_id,
        title=title,
        description=description,
        status=JobStatus.pending
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job
