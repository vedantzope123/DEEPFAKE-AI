# 🛡️ Deepfake AI Detector

A professional-grade deepfake detection tool powered by **Google Gemini 3 Flash API** and **Streamlit**. This application analyzes images and videos for signs of AI-generated manipulation using advanced forensic techniques.

![Deepfake Detector](https://img.shields.io/badge/AI-Gemini%203%20Flash-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-red)

## ✨ Features

- 🎥 **Video & Image Analysis** - Supports MP4, MOV, AVI, JPG, PNG formats
- 🔍 **Forensic Detection** - Analyzes lighting, shadows, facial artifacts, and texture inconsistencies
- 🧠 **AI-Powered Reasoning** - Uses Gemini 3's advanced reasoning capabilities
- 🚫 **Zero Database** - No data storage; all analysis happens in real-time
- 📊 **Confidence Scoring** - Provides percentage-based confidence with detailed explanations
- 🎨 **Modern UI** - Clean, professional interface with dark theme

## 🔬 What It Detects

The AI analyzes media for:

1. **Lighting & Shadows** - Checks if light sources on the subject match the background
2. **Facial Artifacts** - Looks for 'ghosting' around edges, unnatural eye reflections, or irregular blinking
3. **Texture & Noise** - Identifies inconsistent skin textures or digital noise from GAN/Diffusion models
4. **Audio-Visual Sync** - (Videos only) Verifies lip movements align with audio phonemes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one free](https://aistudio.google.com/apikey))

### Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** - Streamlit will automatically open at `http://localhost:8501`

## 🔑 Getting Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key and paste it into the app's sidebar

> **Note:** The API key is free for personal use with generous quotas.

## 📖 How to Use

1. **Enter your API key** in the sidebar
2. **Upload a file** - Choose an image or video
3. **Click "Run Forensic Analysis"** - Wait for the AI to analyze
4. **Review the results** - Check the verdict, confidence score, and detailed explanation

## 🛠️ Technical Details

### Technology Stack

- **Frontend:** Streamlit (Python web framework)
- **AI Model:** Google Gemini 3 Flash Preview (2026)
- **Image Processing:** Pillow (PIL)
- **API Client:** google-genai library

### How It Works

1. **File Upload:** Media is loaded into memory (RAM only)
2. **API Call:** File bytes are sent to Gemini 3 with a forensic prompt
3. **Analysis:** The AI examines frames/pixels for manipulation artifacts
4. **Verdict:** Returns a classification (REAL/FAKE) with reasoning

### Privacy & Security

- ✅ No database - files are never saved
- ✅ No server storage - analysis happens in your session
- ✅ API key stored locally in browser session only
- ✅ Data transmitted only to Google's secure API

## 📁 Project Structure

```
DEEPFAKE AI/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## 🎯 Use Cases

- 🎬 **Media Verification** - Verify authenticity of news footage
- 🖼️ **Social Media** - Check if profile pictures are AI-generated
- 🎓 **Education** - Learn about deepfake detection techniques
- 🔒 **Security** - Pre-screening for suspicious content

## ⚠️ Limitations

- AI analysis should be used as **guidance**, not absolute truth
- Some deepfakes may be sophisticated enough to evade detection
- For critical decisions, consult human forensic experts
- Video analysis requires stable internet for upload

## 🤝 Contributing

This is an educational/demonstration project. Feel free to:

- Report bugs or issues
- Suggest improvements
- Fork and enhance the features

## 📜 License

This project is for educational purposes. The Gemini API has its own terms of service.

## 🔗 Resources

- [Gemini API Documentation](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Guide to Gemini Video Understanding](https://www.youtube.com/watch?v=7iV00Pu3ARg)

## 💡 Future Enhancements

Potential features to add:

- ✨ Frame-by-frame analysis with timestamps
- 📊 Batch processing for multiple files
- 🎨 Heatmap visualization of suspicious areas
- 📈 Historical analysis tracking
- 🔊 Audio deepfake detection

---

**Built with ❤️ using Google Gemini 3 Flash • Powered by Streamlit**

*No data is stored or transmitted beyond the analysis session*
