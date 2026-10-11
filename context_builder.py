from models import (
    Application,
    User,
    UserProfile,
    UserSkill
)


def build_application_context(
    application: Application,
    user: User,
    profile: UserProfile,
    user_skills: list[UserSkill]
) -> dict:

    skills = []

    for user_skill in user_skills:
        skills.append({
            "name": user_skill.skill.name,
            "proficiency": user_skill.proficiency,
            "years_experience": (
                float(user_skill.years_experience)
                if user_skill.years_experience is not None
                else None
            )
        })

    return {
        "application": {
            "company_name": application.company_name,
            "job_title": application.job_title,
            "job_description": application.job_description,
            "status": application.status,
        },
        "candidate": {
            "name": user.name,
            "email": user.email,
            "headline": profile.headline,
            "experience_summary": profile.experience_summary,
            "education": profile.education,
            "resume_text": profile.resume_text,
            "skills": skills
        }
    }


def build_analysis_prompt(context: dict) -> str:

    application = context["application"]
    candidate = context["candidate"]

    skills_text = "\n".join(
        f"- {skill['name']} | "
        f"Proficiency: {skill['proficiency']} | "
        f"Experience: {skill['years_experience']} years"
        for skill in candidate["skills"]
    )

    prompt = f"""
You are analyzing a job application.

CANDIDATE
Name: {candidate["name"]}
Email: {candidate["email"]}
Headline: {candidate["headline"]}

EXPERIENCE
{candidate["experience_summary"]}

EDUCATION
{candidate["education"]}

RESUME
{candidate["resume_text"]}

CANDIDATE SKILLS
{skills_text}

JOB
Company: {application["company_name"]}
Title: {application["job_title"]}

JOB DESCRIPTION
{application["job_description"]}

TASK
Analyze the candidate against the job.

Identify:
1. Required technical skills
2. Required soft skills
3. Important technologies
4. Matched candidate skills
5. Missing or weak skills
6. Likely interview topics

GROUNDING RULES
- Required skills must be supported by the job description.
- Do not invent requirements.
- Only classify a skill as "required" when it is explicitly stated
  or clearly described as a responsibility or requirement.
- Only classify a candidate skill as "matched" when that skill
  appears in the required skills and exists in the candidate context.
- Only classify something as "missing" when it is a required skill
  that the candidate does not have.
- Do not infer unrelated technologies or skills.

Return structured JSON.
"""

    return prompt.strip()