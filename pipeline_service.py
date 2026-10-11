from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models import (
    Application,
    User,
    UserProfile,
    UserSkill,
    PipelineRun,
    AIAnalysis,
)

from context_builder import (
    build_application_context,
    build_analysis_prompt,
)

from gemini_service import (
    analyze_application,
)


MODEL_NAME = "gemini-3.8-flash"
PROMPT_VERSION = "v1"


def run_analysis_pipeline(
    db: Session,
    application: Application
) -> PipelineRun:

    # --------------------------------
    # 1. Create pipeline run
    # --------------------------------

    pipeline_run = PipelineRun(
        application_id=application.id,
        status="PENDING",
    )

    db.add(pipeline_run)
    db.commit()
    db.refresh(pipeline_run)

    try:

        # --------------------------------
        # 2. Start pipeline
        # --------------------------------

        pipeline_run.status = "RUNNING"
        pipeline_run.started_at = datetime.now(timezone.utc)
        pipeline_run.current_step = "LOAD_CONTEXT"

        db.commit()

        # --------------------------------
        # 3. Load candidate
        # --------------------------------

        user = db.get(User, application.user_id)

        if user is None:
            raise ValueError("Application owner not found")

        profile = db.get(
            UserProfile,
            application.user_id
        )

        if profile is None:
            raise ValueError("User profile not found")

        user_skills = (
            db.query(UserSkill)
            .filter(
                UserSkill.user_id == user.id
            )
            .all()
        )

        # --------------------------------
        # 4. Build context
        # --------------------------------

        context = build_application_context(
            application,
            user,
            profile,
            user_skills
        )

        prompt = build_analysis_prompt(context)

        pipeline_run.current_step = "GENERATE_AI_ANALYSIS"

        db.commit()

        # --------------------------------
        # 5. Create AI analysis record
        # --------------------------------

        ai_analysis = AIAnalysis(
            application_id=application.id,
            status="RUNNING",
            model_name=MODEL_NAME,
            prompt_version=PROMPT_VERSION,
        )

        db.add(ai_analysis)
        db.commit()
        db.refresh(ai_analysis)

        # --------------------------------
        # 6. Call Gemini
        # --------------------------------

        result = analyze_application(prompt)

        # --------------------------------
        # 7. Save AI result
        # --------------------------------

        ai_analysis.required_skills = (
            result.required_skills
        )

        ai_analysis.matched_skills = (
            result.matched_skills
        )

        ai_analysis.missing_skills = (
            result.missing_skills
        )

        ai_analysis.interview_topics = (
            result.interview_topics
        )

        ai_analysis.summary = result.summary

        ai_analysis.status = "COMPLETED"

        db.commit()
        db.refresh(ai_analysis)

        # --------------------------------
        # 8. Complete pipeline
        # --------------------------------

        pipeline_run.current_step = "STORE_AI_ANALYSIS"
        pipeline_run.status = "COMPLETED"
        pipeline_run.completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()
        db.refresh(pipeline_run)

        return pipeline_run

    except Exception as error:

        db.rollback()

        pipeline_run.status = "FAILED"
        pipeline_run.error_message = str(error)

        db.add(pipeline_run)
        db.commit()
        db.refresh(pipeline_run)

        return pipeline_run