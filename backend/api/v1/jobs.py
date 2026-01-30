from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from core.dependencies import get_db, get_current_user
from core.enums import JobStatus
from models.job import Job
from models.user import User
from schemas.job import JobCreateRequest, JobViewResponse
from services.job_process import process_job

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"]
)

@router.post("/jobs", response_model=JobViewResponse)
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

@router.get("/jobs", response_model=list[JobViewResponse])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    return jobs

@router.get("/jobs/{job_id}", response_model=JobViewResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(job)
    db.commit()
    return

@router.post("/jobs/{job_id}/run")
def run_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    # Simulate job processing
    job.status = JobStatus.in_progress
    job.result = "Job completed successfully."
    db.commit()

    # TODO: Add job processing logic here
    background_tasks.add_task(process_job, job_id=job_id)
    
    return {"message": "Job is running"}