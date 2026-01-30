from enum import Enum

class JobStatus(Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    failed = 'failed'

class DocumentStatus(Enum):
    uploaded = 'uploaded'
    uploading = 'uploading'
    empty = 'empty'