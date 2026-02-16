"""
FastAPI Backend for Vercel Deployment
Entry point for Vercel serverless functions
"""

import sys
import traceback
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any
import io

# Wrap imports in try-except for better error reporting
genai: Any = None
types: Any = None
GENAI_AVAILABLE = False

try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
    GENAI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: google-genai not available: {e}", file=sys.stderr)
    GENAI_AVAILABLE = False

app = FastAPI(title="Deepfake Detection API")

# Enable CORS for mobile apps and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your mobile app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResponse(BaseModel):
    verdict: str  # "REAL" or "FAKE"
    confidence: str
    analysis: str
    is_fake: bool

FORENSIC_PROMPT = """You are an expert forensic digital media analyst specializing in deepfake detection. Analyze the provided media for inconsistencies in:

1. **Lighting & Shadows:** Check if light sources on the subject match the background.
2. **Facial Artifacts:** Look for 'ghosting' around edges, unnatural eye reflections, or irregular blinking patterns.
3. **Texture & Noise:** Identify inconsistent skin textures or 'digital noise' that suggests GAN/Diffusion generation.
4. **Audio-Visual Sync:** (For Video) Check if lip movements align perfectly with the phonemes in the audio.

Provide a final verdict: **REAL** or **FAKE**, followed by a confidence score (0-100%) and a concise technical explanation."""

@app.get("/")
async def root():
    return {
        "message": "Deepfake Detection API - Powered by Gemini AI",
        "version": "1.0",
        "status": "running",
        "genai_available": GENAI_AVAILABLE,
        "python_version": sys.version,
        "endpoints": {
            "/analyze": "POST - Upload media for analysis",
            "/health": "GET - API health check",
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    }

@app.get("/api")
async def api_root():
    """Alternative root endpoint for /api path"""
    return await root()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "deepfake-detector", "deployment": "vercel"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_media(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    """
    Analyze uploaded media for deepfake detection.
    
    Parameters:
    - file: Image or video file (jpg, png, mp4, mov, avi)
    - api_key: Gemini API key (pass in header or form)
    
    Returns:
    - verdict, confidence, analysis, is_fake
    """
    
    if not GENAI_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Gemini AI library not available. Please contact the administrator."
        )
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'video/mp4', 'video/quicktime', 'video/x-msvideo']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Allowed: {', '.join(allowed_types)}")
    
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Initialize Gemini client
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid API key: {str(e)}")
        
        # Call Gemini API
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[
                    types.Part.from_bytes(data=file_bytes, mime_type=file.content_type),
                    FORENSIC_PROMPT
                ]
            )
        except Exception as e:
            # Try alternative model if the first one fails
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[
                        types.Part.from_bytes(data=file_bytes, mime_type=file.content_type),
                        FORENSIC_PROMPT
                    ]
                )
            except Exception as e2:
                raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e2)}")
        
        result_text = response.text if response.text else "Analysis failed - No response from AI"
        
        # Parse verdict
        is_fake = "FAKE" in result_text.upper()
        verdict = "FAKE" if is_fake else "REAL"
        
        # Try to extract confidence (basic parsing)
        confidence = "N/A"
        if "%" in result_text:
            # Simple extraction - can be improved
            words = result_text.split()
            for i, word in enumerate(words):
                if "%" in word:
                    confidence = word
                    break
        
        return AnalysisResponse(
            verdict=verdict,
            confidence=confidence,
            analysis=result_text,
            is_fake=is_fake
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-with-key-header")
async def analyze_with_header(
    file: UploadFile = File(...),
    authorization: Optional[str] = None
):
    """
    Alternative endpoint using Authorization header for API key.
    Send API key as: Authorization: Bearer YOUR_API_KEY
    """
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    api_key = authorization.replace("Bearer ", "")
    return await analyze_media(file=file, api_key=api_key)

# This is needed for Vercel
handler = app
