import os

from dotenv import load_dotenv
from google import genai

from schemas import AIAnalysisResult


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL_NAME = "gemini-3.8-flash"


def analyze_application(prompt: str) -> AIAnalysisResult:

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": AIAnalysisResult.model_json_schema(),
        },
    )

    if not interaction.output_text:
        raise RuntimeError("Gemini returned an empty response")

    return AIAnalysisResult.model_validate_json(
        interaction.output_text
    )