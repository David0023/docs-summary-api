from pydantic import BaseModel, ConfigDict
from datetime import datetime
from core.enums import JobStatus

class JobBase(BaseModel):
    title: str
    description: str

class JobCreateRequest(JobBase):
    pass

class JobCreateResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    status: JobStatus
    result: str | None = None
    created_at: datetime
    updated_at: datetime