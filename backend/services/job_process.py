from datetime import datetime, timezone
from openai import OpenAI
from core.database import SessionLocal
from models.job import Job
from core.enums import JobStatus
from core.config import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

def process_job(job_id: int):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            # Simulate job processing
            job.status = JobStatus.completed
            job.updated_at = datetime.now(timezone.utc)
            db.commit()
    except Exception as e:
        job.result = f"Job failed with error: {str(e)}"
        job.status = JobStatus.failed
        db.commit()
    finally:
        db.close()