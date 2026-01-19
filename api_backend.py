"""
FastAPI Backend for Mobile Apps
Run with: uvicorn api_backend:app --reload
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel
import io

app = FastAPI(title="Deepfake Detection API")

# Enable CORS for mobile apps
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
        "message": "Deepfake Detection API",
        "version": "1.0",
        "endpoints": {
            "/analyze": "POST - Upload media for analysis",
            "/health": "GET - API health check"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "deepfake-detector"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_media(
    file: UploadFile = File(...),
    api_key: str = None
):
    """
    Analyze uploaded media for deepfake detection.
    
    Parameters:
    - file: Image or video file (jpg, png, mp4, mov, avi)
    - api_key: Gemini API key (pass in header or form)
    
    Returns:
    - verdict, confidence, analysis, is_fake
    """
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'video/mp4', 'video/quicktime', 'video/x-msvideo']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Call Gemini API
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=file.content_type),
                FORENSIC_PROMPT
            ]
        )
        
        result_text = response.text
        
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-with-key-header")
async def analyze_with_header(
    file: UploadFile = File(...),
    authorization: str = None
):
    """
    Alternative endpoint using Authorization header for API key.
    Send API key as: Authorization: Bearer YOUR_API_KEY
    """
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    api_key = authorization.replace("Bearer ", "")
    return await analyze_media(file=file, api_key=api_key)
