from gemini_service import analyze_application


prompt = """
Analyze this job:

Python Backend Developer

Requirements:
- Python
- FastAPI
- PostgreSQL
- REST APIs
- Docker

Return:
- required_skills
- matched_skills
- missing_skills
- interview_topics
- summary

Use only the information provided.
"""

result = analyze_application(prompt)

print("\n===== GEMINI RESULT =====")
print(result.model_dump_json(indent=2))