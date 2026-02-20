"""API backend for Vercel deployment."""

import sys
from typing import Any, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

genai: Any = None
types: Any = None
GENAI_AVAILABLE = False

try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
    GENAI_AVAILABLE = True
except Exception as error:
    print(f"google-genai import failed: {error}", file=sys.stderr)

app = FastAPI(
    title="Deepfake Detection API",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DetectionResult(BaseModel):
    success: bool
    verdict: str
    confidence: str
    analysis: str
    is_fake: bool


FORENSIC_PROMPT = """You are an expert forensic digital media analyst specializing in deepfake detection.
Analyze for lighting mismatch, facial artifacts, texture/noise anomalies, and (for video) lip-sync issues.
Return: VERDICT (REAL/FAKE), CONFIDENCE (%), and a concise technical explanation."""


def _extract_confidence(text: str) -> str:
    if "%" not in text:
        return "N/A"
    for token in text.replace("\n", " ").split():
        if "%" in token:
            return token.strip()
    return "N/A"


async def _analyze(file: UploadFile, api_key: Optional[str]) -> DetectionResult:
    if not GENAI_AVAILABLE:
        raise HTTPException(status_code=503, detail="Gemini library unavailable on server")

    if not api_key:
        raise HTTPException(status_code=400, detail="api_key is required")

    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
    }
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(file_bytes) > int(4.5 * 1024 * 1024):
        raise HTTPException(status_code=400, detail="File too large (max 4.5MB on Vercel)")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            types.Part.from_bytes(data=file_bytes, mime_type=file.content_type),
            FORENSIC_PROMPT,
        ],
    )

    result_text = response.text or "No analysis returned"
    verdict = "FAKE" if "FAKE" in result_text.upper() else "REAL"

    return DetectionResult(
        success=True,
        verdict=verdict,
        confidence=_extract_confidence(result_text),
        analysis=result_text,
        is_fake=(verdict == "FAKE"),
    )


@app.get("/")
@app.get("/api")
@app.get("/api/")
async def api_info() -> dict:
    return {
        "name": "Deepfake Detection API",
        "status": "online",
        "genai_available": GENAI_AVAILABLE,
        "python_version": sys.version.split()[0],
        "endpoints": {
            "health": "/api/health",
            "analyze": "/api/analyze",
            "docs": "/api/docs",
        },
    }


@app.get("/health")
@app.get("/api/health")
async def health() -> dict:
    return {
        "status": "healthy",
        "service": "deepfake-detector",
        "genai": "available" if GENAI_AVAILABLE else "unavailable",
    }


@app.post("/analyze", response_model=DetectionResult)
@app.post("/api/analyze", response_model=DetectionResult)
async def analyze(file: UploadFile = File(...), api_key: Optional[str] = Form(None)) -> DetectionResult:
    try:
        return await _analyze(file=file, api_key=api_key)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {error}")


handler = app
