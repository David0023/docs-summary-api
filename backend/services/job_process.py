from datetime import datetime, timezone
from openai import OpenAI
from core.database import SessionLocal
from models.job import Job
from models.document import Document
from core.enums import JobStatus
from core.config import settings
from utils.file import delete_file

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

def process_job(job_id: int):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        documents = db.query(Document).filter(Document.job_id == job_id).all()
        if job:
            # Simulate job processing
            # TODO: Add actual processing logic here
            job.status = JobStatus.completed
            job.updated_at = datetime.now(timezone.utc)
            job.result = "Job processed successfully."

            # Clean up document files after processing
            for doc in documents:
                delete_file(doc.filepath)        
                db.delete(doc)
            db.commit()
    except Exception as e:
        job.result = f"Job failed with error: {str(e)}"
        job.status = JobStatus.failed
        db.commit()
    finally:
        db.close()