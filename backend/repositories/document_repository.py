from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.document import Document
from core.enums import JobStatus

async def get_one_document(db: AsyncSession, **kwargs) -> Document | None:
    query = select(Document).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_many_documents(db: AsyncSession, **kwargs) -> List[Document]:
    query = select(Document).filter_by(**kwargs)
    result = await db.execute(query)
    return result.scalars().all()

async def create_document(db: AsyncSession, job_id: int, filename: str, filepath: str, content_type: str) -> Document:
    new_document = Document(
        job_id=job_id,
        filename=filename,
        filepath=filepath,
        content_type=content_type,
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document
