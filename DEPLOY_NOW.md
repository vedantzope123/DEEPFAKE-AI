# 🚀 Quick Deployment Guide for Vercel

## ✅ Your Project is Ready!

The API is tested and working locally. Here's how to deploy:

## 📦 What Was Fixed:

1. ✅ Created `runtime.txt` - Specifies Python 3.11
2. ✅ Updated `api/index.py` - Added robust error handling  
3. ✅ Updated `requirements.txt` - Compatible dependency versions
4. ✅ Created `vercel.json` - Vercel configuration
5. ✅ Added `.vercelignore` - Excludes unnecessary files
6. ✅ **Tested locally** - API runs successfully on port 8000

## 🌐 Deploy to Vercel Now:

### Option 1: GitHub + Vercel Dashboard (Easiest)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Ready for Vercel deployment"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your repository
   - Click "Deploy"
   - Wait 2-3 minutes ✨

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (from your project folder)
cd "c:\Users\dell\OneDrive\Desktop\DEEPFAKE AI"
vercel --prod
```

## 🧪 Test Your Deployed API:

Once deployed, Vercel will give you a URL like: `https://your-project.vercel.app`

### Test the root endpoint:
```bash
curl https://your-project.vercel.app/
```

Expected response:
```json
{
  "message": "Deepfake Detection API - Powered by Gemini AI",
  "version": "1.0",
  "status": "running",
  "genai_available": true,
  "python_version": "3.11.x",
  "endpoints": {
    "/analyze": "POST - Upload media for analysis",
    "/health": "GET - API health check",
    "/docs": "GET - API documentation (Swagger UI)",
    "/redoc": "GET - API documentation (ReDoc)"
  }
}
```

## 📡 API Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and health |
| `/health` | GET | Health check |
| `/analyze` | POST | Upload media for analysis |
| `/docs` | GET | Interactive API docs (Swagger) |
| `/redoc` | GET | API documentation (ReDoc) |

## 🎯 Example API Usage:

### Using cURL:
```bash
curl -X POST "https://your-project.vercel.app/analyze" \
  -F "file=@path/to/image.jpg" \
  -F "api_key=YOUR_GEMINI_API_KEY"
```

### Using Python:
```python
import requests

url = "https://your-project.vercel.app/analyze"
files = {"file": open("image.jpg", "rb")}
data = {"api_key": "YOUR_GEMINI_API_KEY"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Using JavaScript/Fetch:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('api_key', 'YOUR_GEMINI_API_KEY');

fetch('https://your-project.vercel.app/analyze', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🔑 Environment Variables (Optional):

To secure your API key:

1. In Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add variable:
   - Name: `GEMINI_API_KEY`
   - Value: `your_actual_api_key`
3. Redeploy

Then update your code to use it as default:
```python
api_key = os.getenv('GEMINI_API_KEY', api_key)
```

## ⚠️ Important Notes:

### Vercel Free Tier Limits:
- ⏱️ 10-second function timeout
- 📦 250MB deployment size limit
- 📁 4.5MB request body limit
- 🌐 100GB bandwidth/month

### File Upload Limits:
- Maximum file size: **4.5MB** (Vercel limit)
- For larger files: Use Vercel Blob Storage or compress before upload

### Supported File Types:
- Images: JPG, JPEG, PNG
- Videos: MP4, MOV, AVI

## 🐛 Troubleshooting:

### "FUNCTION_INVOCATION_FAILED" Error:
✅ **FIXED!** Added proper error handling and imports

### 404 Error:
- Ensure `api/index.py` exists
- Check `vercel.json` configuration
- Try redeploying

### Timeout Error:
- Use smaller test files (< 4MB)
- Consider upgrading Vercel plan for longer timeouts

### Check Vercel Logs:
```bash
vercel logs YOUR_DEPLOYMENT_URL
```

Or in Vercel Dashboard: Your Project → Deployments → Click deployment → View Function Logs

## 📱 Mobile App Integration:

See `mobile_integration_guide.md` for React Native, Flutter, iOS, and Android examples.

## 🎉 Next Steps:

1. Deploy to Vercel using one of the methods above
2. Test all endpoints
3. Integrate with your mobile app or frontend
4. (Optional) Add authentication/rate limiting
5. (Optional) Add custom domain

## 📚 Resources:

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gemini API Docs](https://ai.google.dev/docs)

---

**Your API is ready to deploy! 🚀**

Any issues? Check the Vercel deployment logs for detailed error messages.
