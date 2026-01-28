from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreateRequest(UserBase):
    password: str

class UserCreateResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

