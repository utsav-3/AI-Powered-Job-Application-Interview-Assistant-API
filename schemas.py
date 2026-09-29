from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):

    user_id: UUID
    company_name: str
    job_title: str
    job_description: str


class ApplicationResponse(BaseModel):

    id: UUID
    user_id: UUID
    company_name: str
    job_title: str
    job_description: str
    status: str
    applied_at: datetime

    model_config = ConfigDict(from_attributes=True)