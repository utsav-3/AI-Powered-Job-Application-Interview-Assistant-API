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


class PipelineStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class PipelineRunResponse(BaseModel):
    id: UUID
    application_id: UUID
    status: PipelineStatus
    current_step: str | None
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class AIAnalysisResult(BaseModel):
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    interview_topics: list[str]
    summary: str