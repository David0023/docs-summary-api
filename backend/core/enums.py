from enum import Enum

class JobStatus(Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    completed = 'completed'
    failed = 'failed'