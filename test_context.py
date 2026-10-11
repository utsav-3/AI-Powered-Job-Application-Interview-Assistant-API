from database import SessionLocal
from models import Application, User, UserProfile, UserSkill


from context_builder import (
    build_application_context,
    build_analysis_prompt
)


db = SessionLocal()

try:

    application = db.query(Application).first()

    if application is None:
        raise Exception("No application found")

    user = db.get(User, application.user_id)

    if user is None:
        raise Exception("User not found")

    profile = db.get(
        UserProfile,
        application.user_id
    )

    if profile is None:
        raise Exception("User profile not found")

    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user.id)
        .all()
    )

    context = build_application_context(
        application,
        user,
        profile,
        user_skills
    )

    print("\n===== CONTEXT =====")
    print(context)

    prompt = build_analysis_prompt(context)

    print("\n===== PROMPT =====")
    print(prompt)

finally:
    db.close()