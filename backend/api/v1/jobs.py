from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.auth import get_current_user
from core.enums import JobStatus
from models.job import Job
from models.user import User
from schemas.job import JobCreateResponse, JobCreateRequest

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

@router.post("/jobs", response_model=JobCreateResponse)
def create_jobs(
    db: Session = Depends(get_db),
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
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/jobs", response_model=list[JobCreateResponse])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    return jobs