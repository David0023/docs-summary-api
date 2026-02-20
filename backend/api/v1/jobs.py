from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_db, get_current_user
from core.enums import JobStatus
from models.job import Job
from models.document import Document
from models.user import User
from schemas.job import JobCreateRequest, JobViewResponse
from services.job_process import process_job
from utils.file import delete_file

from repositories.job_repository import get_one_job, get_many_jobs
from repositories.document_repository import get_one_document, get_many_documents, create_document

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

@router.post("/jobs", response_model=JobViewResponse)
async def create_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    job_request: JobCreateRequest = Depends()
):
    new_job = Job(
        user_id=current_user.id,
        title=job_request.title,
        description=job_request.description,
        status=JobStatus.pending
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job

@router.get("/jobs", response_model=list[JobViewResponse])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_many_jobs(db, user_id=current_user.id)

@router.get("/jobs/{job_id}", response_model=JobViewResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = await get_one_job(db, id=job_id, user_id=current_user.id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = await get_one_job(db, id=job_id, user_id=current_user.id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    docs = await get_many_documents(db, job_id=job_id)
    for doc in docs:
        delete_file(doc.filepath)
        await db.delete(doc)
    await db.delete(job)
    await db.commit()
    return

@router.post("/jobs/{job_id}/run")
async def run_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = await get_one_job(db, id=job_id, user_id=current_user.id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    # Simulate job processing
    job.status = JobStatus.in_progress
    job.result = "Job completed successfully."
    await db.commit()

    # TODO: Add job processing logic here
    background_tasks.add_task(process_job, job_id=job_id)
    
    return {"message": "Job is running"}