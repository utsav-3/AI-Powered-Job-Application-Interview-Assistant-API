from datetime import datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SCREENING = "SCREENING"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class ApplicationCreate(BaseModel):
    user_id: UUID
    company_name: str
    job_title: str
    job_description: str


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    company_name: str
    job_title: str
    job_description: str
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)