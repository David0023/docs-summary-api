from models.base import BaseModel, TimestampMixin
from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum, ForeignKey

from core.enums import DocumentStatus


class Document(BaseModel):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # Multiple documents can be attached to a single job
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # Original file name
    filename = Column(String(255), nullable=False)

    # Saved file path (name randomized for uniqueness)
    filepath = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    status = Column(SqlEnum(DocumentStatus), default=DocumentStatus.empty, nullable=False)