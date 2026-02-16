# Vercel Deployment Guide

Your project is now configured for Vercel deployment!

## 📁 Project Structure
```
DEEPFAKE AI/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── api_backend.py        # Original FastAPI backend (for local development)
├── app.py                # Streamlit app (for local development)
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies for Vercel
└── .vercelignore         # Files to ignore during deployment
```

## 🚀 How to Deploy to Vercel

### Method 1: Deploy via Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub, GitLab, or Bitbucket
3. Click "Add New Project"
4. Import your GitHub repository
5. Vercel will auto-detect the configuration
6. Click "Deploy"

### Method 2: Deploy via Vercel CLI
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to your project directory:
   ```bash
   cd "c:\Users\dell\OneDrive\Desktop\DEEPFAKE AI"
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy:
   ```bash
   vercel
   ```

5. For production deployment:
   ```bash
   vercel --prod
   ```

## 📡 API Endpoints

Once deployed, your API will be available at: `https://your-project.vercel.app`

### Endpoints:
- `GET /` - API information and available endpoints
- `GET /health` - Health check
- `POST /analyze` - Upload media for deepfake detection
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

### Example Usage:
```bash
curl -X POST "https://your-project.vercel.app/analyze" \
  -F "file=@image.jpg" \
  -F "api_key=YOUR_GEMINI_API_KEY"
```

## 🔑 Environment Variables (Optional)

If you want to store your Gemini API key as an environment variable:

1. In Vercel Dashboard, go to your project
2. Settings → Environment Variables
3. Add: `GEMINI_API_KEY` = `your_api_key_here`

Then modify the code to use `os.getenv('GEMINI_API_KEY')` as a fallback.

## 🧪 Local Development

To run locally:

### FastAPI Backend:
```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```
Access at: http://localhost:8000

### Streamlit App:
```bash
pip install streamlit google-genai pillow
streamlit run app.py
```
Access at: http://localhost:8501

## ⚠️ Important Notes

1. **Vercel Free Tier Limits:**
   - 10-second function timeout
   - 250MB deployment size
   - For larger files/longer processing, consider upgrading

2. **API Key Security:**
   - Never commit API keys to GitHub
   - Use environment variables for production
   - The current implementation accepts API key from client (for mobile apps)

3. **File Upload Limits:**
   - Default: 4.5MB (Vercel body size limit)
   - For larger files, use Vercel Blob Storage or external storage

## 🛠️ Troubleshooting

### 404 Error:
- Make sure `api/index.py` exists
- Check `vercel.json` configuration
- Redeploy the project

### Deployment Fails:
- Check requirements.txt for incompatible packages
- Ensure all dependencies are compatible with Python 3.9+

### Function Timeout:
- Optimize video processing
- Use smaller file sizes
- Consider upgrading Vercel plan

## 📱 Mobile Integration

See `mobile_integration_guide.md` for instructions on integrating with mobile apps (React Native, Flutter, iOS, Android).

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
