from models.base import BaseModel, TimestampMixin
from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum, ForeignKey

from sqlalchemy.orm import relationship

from core.enums import JobStatus

class Job(BaseModel, TimestampMixin):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SqlEnum(JobStatus), default=JobStatus.pending, nullable=False)
    result = Column(Text, nullable=True)

    documents = relationship("Document", back_populates="job")