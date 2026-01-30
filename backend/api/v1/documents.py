from magic import from_buffer
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from core.config import settings
from core.dependencies import get_db, get_current_user
from core.enums import DocumentStatus
from models.document import Document

from models.user import User
from models.job import Job
from utils.file import save_file
from schemas.document import DocumentAttachResponse


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.post("/attach/{job_id}", response_model=DocumentAttachResponse)
async def attach_document(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    actual_type = from_buffer(content, mime=True)
    if actual_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported file type: {actual_type}")
    if file.content_type and actual_type != file.content_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content type mismatch")

    filepath = save_file(content)

    new_document = Document(
        job_id=job_id,
        filename=file.filename,
        filepath=filepath,
        content_type=actual_type,
        status=DocumentStatus.uploaded
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document