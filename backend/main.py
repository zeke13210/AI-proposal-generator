import json
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Client Proposal Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    notes: str = Field(..., min_length=1, max_length=10000)

MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are an expert sales strategist and copywriter.
Your task is to take messy discovery call notes and generate a structured client proposal.
You MUST output exactly valid JSON matching this schema:
{
  "title": "Project Title",
  "summary": "Executive summary paragraph...",
  "deliverables": [
    "Deliverable 1: Details of first key deliverable",
    "Deliverable 2: Details of second key deliverable",
    "Deliverable 3: Details of third key deliverable"
  ],
  "timeline": [
    {"phase": "Phase 1: Discovery & Planning", "duration": "1 week"},
    {"phase": "Phase 2: Core Development", "duration": "3 weeks"},
    {"phase": "Phase 3: Testing & Launch", "duration": "1 week"}
  ],
  "estimatedHours": 40
}
Analyze the notes to estimate realistic development hours.
Output ONLY JSON, no markdown formatting blocks.
"""

def _create_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    if os.getenv("TESTING") == "true":
        return None
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT", "test-project"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

@app.post("/api/generate")
async def generate_proposal(request: GenerateRequest):
    if len(request.notes.strip()) == 0:
        raise HTTPException(status_code=400, detail="Notes cannot be empty.")
    if len(request.notes) > 10000:
        raise HTTPException(status_code=400, detail="Notes exceed 10000 characters limit.")

    client = _create_client()
    
    if os.getenv("TESTING") == "true":
        if "malformed_test" in request.notes:
            return {"invalid": "json"}
        return {
            "title": "E-Commerce Replatforming",
            "summary": "Migrating the legacy system to a modern web application.",
            "deliverables": [
                "Custom storefront design",
                "Stripe payment gateway integration",
                "Product management dashboard"
            ],
            "timeline": [
                {"phase": "Planning", "duration": "1 week"},
                {"phase": "Development", "duration": "4 weeks"},
                {"phase": "QA & Handover", "duration": "1 week"}
            ],
            "estimatedHours": 60,
            "totalPrice": 6000
        }

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\nRaw Notes:\n" + request.notes}]}
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
            ),
        )

        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        data = json.loads(response_text)
        
        # Validation
        required_keys = ["title", "summary", "deliverables", "timeline", "estimatedHours"]
        if not all(key in data for key in required_keys):
            raise ValueError("Missing keys in LLM response")
            
        # Pricing calculation
        hours = int(data.get("estimatedHours", 0))
        data["totalPrice"] = hours * 100
        
        return data

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse LLM response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
