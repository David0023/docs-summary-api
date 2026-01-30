from fastapi import File
from pydantic import BaseModel, ConfigDict
from core.enums import DocumentStatus

class DocumentAttachResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    job_id: int
    filename: str
    filepath: str
    content_type: str
    status: DocumentStatus