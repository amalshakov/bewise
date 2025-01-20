from datetime import datetime

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    user_name: str
    description: str


class ApplicationResponse(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime
