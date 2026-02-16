"""
Deepfake Detection API - Production Ready
Rebuilt from scratch for Vercel deployment
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Any
import traceback
import sys

# Try to import Gemini AI
genai: Any = None
types: Any = None
GENAI_AVAILABLE = False

try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
    GENAI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ google-genai not available: {e}", file=sys.stderr)

# Initialize FastAPI app
app = FastAPI(
    title="🔍 Deepfake Detection API",
    description="AI-powered deepfake detection using Google Gemini AI",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response model
class DetectionResult(BaseModel):
    """Response structure for deepfake detection"""
    success: bool
    verdict: str
    confidence: str
    analysis: str
    is_fake: bool
    error: Optional[str] = None

# AI Forensic Prompt
FORENSIC_PROMPT = """You are an expert forensic digital media analyst specializing in deepfake detection. 

Analyze this media for inconsistencies in:
1. **Lighting & Shadows** - Check if light sources match the background
2. **Facial Artifacts** - Look for ghosting, unnatural reflections, irregular blinking
3. **Texture & Noise** - Identify inconsistent skin textures or digital noise
4. **Audio-Visual Sync** - (Video only) Check lip-sync accuracy

Provide your analysis in this format:
VERDICT: [REAL or FAKE]
CONFIDENCE: [percentage]%
ANALYSIS: [detailed technical explanation]
"""

# HTML frontend
HTML_FRONTEND = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Deepfake Detector</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        .result.show {
            display: block;
        }
        .result.real {
            background: #d4edda;
            border: 2px solid #28a745;
        }
        .result.fake {
            background: #f8d7da;
            border: 2px solid #dc3545;
        }
        .verdict {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .verdict.real { color: #28a745; }
        .verdict.fake { color: #dc3545; }
        .confidence {
            font-size: 18px;
            margin-bottom: 15px;
            color: #555;
        }
        .analysis {
            color: #333;
            line-height: 1.6;
        }
        .error {
            background: #fff3cd;
            border: 2px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .loading {
            text-align: center;
            margin-top: 20px;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .api-info {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        .api-info a {
            color: #667eea;
            text-decoration: none;
            margin: 0 10px;
        }
        .api-info a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Deepfake Detector</h1>
        <p class="subtitle">AI-Powered Media Verification</p>
        
        <form id="uploadForm">
            <div class="form-group">
                <label for="apiKey">Gemini API Key:</label>
                <input type="text" id="apiKey" placeholder="Enter your Gemini API key" required>
            </div>
            
            <div class="form-group">
                <label for="mediaFile">Upload Image or Video:</label>
                <input type="file" id="mediaFile" accept="image/*,video/*" required>
            </div>
            
            <button type="submit">Analyze Media</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; color: #666;">Analyzing media...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <div class="verdict" id="verdict"></div>
            <div class="confidence" id="confidence"></div>
            <div class="analysis" id="analysis"></div>
        </div>
        
        <div class="api-info">
            <a href="/docs" target="_blank">📚 API Docs</a>
            <a href="/health" target="_blank">❤️ Health Check</a>
        </div>
    </div>

    <script>
        const form = document.getElementById('uploadForm');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const result = document.getElementById('result');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const apiKey = document.getElementById('apiKey').value;
            const fileInput = document.getElementById('mediaFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showError('Please select a file');
                return;
            }
            
            // Reset UI
            loading.classList.add('show');
            error.classList.remove('show');
            result.classList.remove('show');
            
            // Create form data
            const formData = new FormData();
            formData.append('file', file);
            formData.append('api_key', apiKey);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.classList.remove('show');
                
                if (response.ok) {
                    showResult(data);
                } else {
                    showError(data.detail || 'Analysis failed');
                }
            } catch (err) {
                loading.classList.remove('show');
                showError('Network error: ' + err.message);
            }
        });
        
        function showResult(data) {
            const verdict = document.getElementById('verdict');
            const confidence = document.getElementById('confidence');
            const analysis = document.getElementById('analysis');
            
            verdict.textContent = data.verdict;
            verdict.className = 'verdict ' + (data.is_fake ? 'fake' : 'real');
            
            confidence.textContent = 'Confidence: ' + data.confidence;
            analysis.textContent = data.analysis;
            
            result.className = 'result show ' + (data.is_fake ? 'fake' : 'real');
        }
        
        function showError(message) {
            error.textContent = '⚠️ ' + message;
            error.classList.add('show');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web interface"""
    return HTML_FRONTEND

@app.get("/api")
@app.get("/api/")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Deepfake Detection API",
        "version": "2.0.0",
        "status": "online",
        "genai_available": GENAI_AVAILABLE,
        "python_version": sys.version.split()[0],
        "endpoints": {
            "/": "Web interface",
            "/analyze": "POST - Analyze media for deepfakes",
            "/health": "GET - Health check",
            "/docs": "GET - Interactive API documentation",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "deepfake-detector",
        "genai": "available" if GENAI_AVAILABLE else "unavailable",
        "deployment": "vercel"
    }

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
) -> DetectionResult:
    """
    Analyze uploaded media for deepfake detection
    
    Args:
        file: Image or video file (JPG, PNG, MP4, MOV, AVI)
        api_key: Your Gemini API key
    
    Returns:
        DetectionResult with verdict, confidence, and analysis
    """
    
    # Check if Gemini is available
    if not GENAI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Gemini AI is not available. Please check server configuration."
        )
    
    # Validate API key
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="API key is required. Get one at https://aistudio.google.com/apikey"
        )
    
    # Validate file type
    allowed_types = {
        'image/jpeg', 'image/jpg', 'image/png',
        'video/mp4', 'video/quicktime', 'video/x-msvideo'
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}"
        )
    
    try:
        # Read file
        file_bytes = await file.read()
        
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        if len(file_bytes) > 4.5 * 1024 * 1024:  # 4.5MB limit for Vercel
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 4.5MB for Vercel deployment."
            )
        
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Analyze with Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=file.content_type),
                FORENSIC_PROMPT
            ]
        )
        
        # Get result
        result_text = response.text if response.text else "No analysis returned"
        
        # Parse verdict
        verdict = "FAKE" if "FAKE" in result_text.upper() else "REAL"
        is_fake = verdict == "FAKE"
        
        # Extract confidence
        confidence = "N/A"
        if "%" in result_text:
            words = result_text.split()
            for word in words:
                if "%" in word:
                    confidence = word.strip()
                    break
        
        return DetectionResult(
            success=True,
            verdict=verdict,
            confidence=confidence,
            analysis=result_text,
            is_fake=is_fake
        )
        
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# Vercel handler
handler = app
