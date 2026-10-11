import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


application_status = ENUM(
    "APPLIED",
    "SCREENING",
    "INTERVIEW",
    "OFFER",
    "REJECTED",
    "WITHDRAWN",
    name="application_status",
    create_type=False
)


class User(Base):

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String(100), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    profile = relationship(
    "UserProfile",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
    )

    skills = relationship(
    "UserSkill",
    back_populates="user",
    cascade="all, delete-orphan"
)
class UserProfile(Base):

    __tablename__ = "user_profiles"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    headline = Column(
        String(200),
        nullable=True
    )

    experience_summary = Column(
        Text,
        nullable=True
    )

    education = Column(
        Text,
        nullable=True
    )

    resume_text = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="profile"
    )

class Application(Base):

    __tablename__ = "applications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    company_name = Column(
        String(150),
        nullable=False
    )

    job_title = Column(
        String(150),
        nullable=False
    )

    job_description = Column(
        Text,
        nullable=False
    )

    status = Column(
        application_status,
        nullable=False,
        server_default="APPLIED"
    )

    applied_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class AIAnalysis(Base):

    __tablename__ = "ai_analyses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "applications.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    status = Column(
        ENUM(
            "PENDING",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            name="ai_analysis_status",
            create_type=False
        ),
        nullable=False,
        server_default="PENDING"
    )

    match_score = Column(
        Numeric(5, 2),
        nullable=True
    )

    required_skills = Column(
        JSONB,
        nullable=True
    )

    matched_skills = Column(
        JSONB,
        nullable=True
    )

    missing_skills = Column(
        JSONB,
        nullable=True
    )

    interview_topics = Column(
        JSONB,
        nullable=True
    )

    summary = Column(
        Text,
        nullable=True
    )

    model_name = Column(
        String(100),
        nullable=True
    )

    prompt_version = Column(
        String(50),
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
class PipelineRun(Base):

    __tablename__ = "pipeline_runs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "applications.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    status = Column(
        ENUM(
            "PENDING",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            name="pipeline_status",
            create_type=False
        ),
        nullable=False,
        server_default="PENDING"
    )

    current_step = Column(
        String(100),
        nullable=True
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
class Skill(Base):

    __tablename__ = "skills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user_skills = relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
class UserSkill(Base):

    __tablename__ = "user_skills"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True
    )

    proficiency = Column(
        String(50),
        nullable=True
    )

    years_experience = Column(
        Numeric(4, 1),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="skills"
    )

    skill = relationship(
        "Skill",
        back_populates="user_skills"
    )