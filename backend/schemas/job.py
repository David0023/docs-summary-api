from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import JobStatus
from schemas.document import DocumentAttachResponse

class JobBase(BaseModel):
    title: str
    description: str

class JobCreateRequest(JobBase):
    pass

class JobViewResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: JobStatus
    result: str | None = None
    created_at: datetime
    updated_at: datetime
    documents: list[DocumentAttachResponse] = []