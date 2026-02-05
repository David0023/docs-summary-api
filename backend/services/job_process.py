from datetime import datetime, timezone
from fastapi import HTTPException, status
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
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        if job.status != JobStatus.in_progress:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job is not in progress status")

        result = ""
        with OpenAI() as client:
            content = [{"type": "text", "text": "Summarize the following documents."}]
            
            # 1. File upload and ID collection
            uploaded_file_ids = []
            for doc in documents:
                with open(doc.filepath, "rb") as f:
                    uploaded_file = client.files.create(file=f, purpose='assistants')
                    uploaded_file_ids.append(uploaded_file.id)
                    
                    # Content array for the request
                    content.append({
                        "type": "file", 
                            "file": {
                            "file_id": uploaded_file.id
                        }
                    })

            # 2. Chat Completion 요청
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": content}]
            )

            result = response.choices[0].message.content

            # 3. Open AI Server file delete
            for f_id in uploaded_file_ids:
                try:
                    client.files.delete(f_id)
                except:
                    pass 

        # Update job status and result
        job.status = JobStatus.completed
        job.updated_at = datetime.now(timezone.utc)
        job.result = result

        # Clean up document files after processing
        for doc in documents:
            delete_file(doc.filepath)
            db.delete(doc)
        db.commit()

    except Exception as e:
        db.rollback()
        job.result = f"Job failed with error: {str(e)}"
        job.status = JobStatus.failed
        db.commit()
    finally:
        db.close()