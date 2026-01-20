import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Gemini Forensic AI", page_icon="🔍", layout="wide")

# Initialize session state for welcome page
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

# --- WELCOME PAGE ---
if st.session_state.show_welcome:
    # Apply custom CSS with bubbles animation
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow: hidden;
            position: relative;
        }
        
        /* Bubbles Animation */
        .bubbles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }
        
        .bubble {
            position: absolute;
            bottom: -100px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            opacity: 0.5;
            animation: rise 15s infinite ease-in;
        }
        
        .bubble:nth-child(1) {
            width: 40px;
            height: 40px;
            left: 10%;
            animation-duration: 8s;
        }
        
        .bubble:nth-child(2) {
            width: 20px;
            height: 20px;
            left: 20%;
            animation-duration: 5s;
            animation-delay: 1s;
        }
        
        .bubble:nth-child(3) {
            width: 50px;
            height: 50px;
            left: 35%;
            animation-duration: 7s;
            animation-delay: 2s;
        }
        
        .bubble:nth-child(4) {
            width: 80px;
            height: 80px;
            left: 50%;
            animation-duration: 11s;
            animation-delay: 0s;
        }
        
        .bubble:nth-child(5) {
            width: 35px;
            height: 35px;
            left: 55%;
            animation-duration: 6s;
            animation-delay: 1s;
        }
        
        .bubble:nth-child(6) {
            width: 45px;
            height: 45px;
            left: 65%;
            animation-duration: 8s;
            animation-delay: 3s;
        }
        
        .bubble:nth-child(7) {
            width: 90px;
            height: 90px;
            left: 70%;
            animation-duration: 12s;
            animation-delay: 2s;
        }
        
        .bubble:nth-child(8) {
            width: 25px;
            height: 25px;
            left: 80%;
            animation-duration: 6s;
            animation-delay: 2s;
        }
        
        .bubble:nth-child(9) {
            width: 15px;
            height: 15px;
            left: 70%;
            animation-duration: 5s;
            animation-delay: 1s;
        }
        
        .bubble:nth-child(10) {
            width: 90px;
            height: 90px;
            left: 25%;
            animation-duration: 10s;
            animation-delay: 4s;
        }
        
        @keyframes rise {
            0% {
                bottom: -100px;
                transform: translateX(0);
            }
            50% {
                transform: translateX(100px);
            }
            100% {
                bottom: 1080px;
                transform: translateX(-200px);
            }
        }
        
        .welcome-content {
            position: relative;
            z-index: 1;
        }
        
        /* Glowing text animation */
        @keyframes glow {
            0%, 100% {
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.5), 0 0 30px rgba(0, 212, 255, 0.5);
            }
            50% {
                text-shadow: 0 0 30px rgba(255, 255, 255, 0.8), 0 0 40px rgba(0, 212, 255, 0.8);
            }
        }
        
        .bilingual-title {
            animation: glow 3s ease-in-out infinite;
        }
        </style>
        
        <!-- Bubbles Background -->
        <div class="bubbles">
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
            <div class="bubble"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create welcome content using Streamlit native components
    st.markdown("<div class='welcome-content'>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Title with custom styling - Bilingual (Hindi + English)
    st.markdown("""
        <h1 style='text-align: center; font-size: 3.5rem; font-weight: 800; 
        color: #fff; margin-bottom: 10px;' class='bilingual-title'>
        🛡️ स्वागत है | WELCOME
        </h1>
    """, unsafe_allow_html=True)
    
    # Subtitle
    st.markdown("""
        <h2 style='text-align: center; font-size: 1.8rem; color: #e0e7ff; 
        font-weight: 300; margin-bottom: 15px;'>
        Deepfake AI Video & Image Detector
        </h2>
        <h3 style='text-align: center; font-size: 1.3rem; color: #d0d7ff; 
        font-weight: 300; margin-bottom: 30px;'>
        डीपफेक  एआई  वीडियो  और  छवि  डिटेक्टर
        </h3>
    """, unsafe_allow_html=True)
    
    # Designer info card
    st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); 
        border-radius: 20px; padding: 30px; margin: 40px auto; max-width: 600px; 
        border: 2px solid rgba(255, 255, 255, 0.2); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        text-align: center;'>
            <div style='font-size: 2rem; font-weight: 600; color: #fff; margin-bottom: 15px;'>
               <h2> Designed by Vedant Zope</h2>
            </div>
            <div style='display: inline-block; background: linear-gradient(45deg, #ff6b6b, #ee5a6f);
            padding: 10px 25px; border-radius: 25px; font-size: 1.1rem; margin: 20px 0;'>
                ⚙️ Still Working On It
            </div>
            <div style='display: flex; align-items: center; justify-content: center; 
            gap: 15px; margin-top: 25px; font-size: 1.3rem;'>
                <span style='font-size: 2rem;'>🔗</span>
                <a href='https://instagram.com/offx.vedanthh' target='_blank' 
                style='color: #fff; font-weight: 500; text-decoration: none;'>
                    @offx.vedanthh
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Custom styled button
    st.markdown("""
        <style>
        div.stButton > button {
            width: 300px;
            height: 60px;
            border-radius: 30px;
            background: linear-gradient(45deg, #00c6ff, #0072ff);
            color: white;
            border: none;
            font-size: 1.3rem;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(0, 114, 255, 0.4);
            margin: 0 auto;
            display: block;
        }
        div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 114, 255, 0.6);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started", key="start_btn"):
            st.session_state.show_welcome = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN APP STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Deepfake AI Video & Image Detector")
st.write("Upload Video or Images to Analyze Media Authenticity using Gemini 3 Flash AI")

# --- SIDEBAR & API KEY ---
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("No data is stored. Analysis happens in real-time.")
    
    st.markdown("---")
    st.markdown("### About This Tool")
    st.markdown("""
    This tool uses Google's Gemini 3 Flash AI to detect deepfakes by analyzing:
    - **Lighting & Shadows:** Consistency with background
    - **Facial Artifacts:** Ghosting, eye reflections, blinking
    - **Texture & Noise:** GAN/Diffusion generation artifacts
    - **Audio-Visual Sync:** Lip movement alignment (for videos)
    """)
    
    st.markdown("---")
    st.markdown("### How to Get API Key")
    st.markdown("""
    1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
    2. Sign in with your Google account
    3. Click "Create API Key"
    4. Copy and paste it above
    """)

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Choose a Video or Image...", type=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png'])

if uploaded_file and api_key:
    client = genai.Client(api_key=api_key)
    
    # Display the uploaded media
    if uploaded_file.type.startswith('video'):
        st.video(uploaded_file)
        mime_type = uploaded_file.type
    else:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)
        mime_type = uploaded_file.type

    if st.button("🔍 Run Forensic Analysis"):
        with st.spinner("Analyzing media artifacts..."):
            try:
                # Read file bytes
                file_bytes = uploaded_file.getvalue()
                
                # Expert forensic prompt for deepfake detection
                forensic_prompt = """You are an expert forensic digital media analyst specializing in deepfake detection. Analyze the provided media for inconsistencies in:

1. **Lighting & Shadows:** Check if light sources on the subject match the background.
2. **Facial Artifacts:** Look for 'ghosting' around edges, unnatural eye reflections, or irregular blinking patterns.
3. **Texture & Noise:** Identify inconsistent skin textures or 'digital noise' that suggests GAN/Diffusion generation.
4. **Audio-Visual Sync:** (For Video) Check if lip movements align perfectly with the phonemes in the audio.

Provide a final verdict: **REAL** or **FAKE**, followed by a confidence score (0-100%) and a concise technical explanation."""
                
                # Call Gemini 3 API (Latest 2026 reasoning model)
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[
                        types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                        forensic_prompt
                    ]
                )
                
                # --- ATTRACTIVE RESULT DISPLAY ---
                st.markdown("---")
                st.subheader("🎯 Forensic Analysis Results")
                result_text = response.text
                
                # Determine verdict based on response
                if "FAKE" in result_text.upper():
                    st.error("🚩 **Potential Deepfake Detected**")
                    st.markdown("### ⚠️ This media shows signs of manipulation")
                else:
                    st.success("✅ **Likely Authentic Media**")
                    st.markdown("### ✓ No significant manipulation detected")
                
                # Display detailed analysis
                st.markdown("### 📋 Detailed Analysis Report")
                st.markdown(f"> {result_text}")
                
                # Additional info box
                st.info("💡 **Note:** This analysis is AI-powered and should be used as a guidance tool. For critical decisions, consult with human forensic experts.")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                st.markdown("""
                **Troubleshooting:**
                - Ensure your API key is valid
                - Check if the file format is supported
                - Verify your internet connection
                - Try with a smaller file size
                """)
                
elif not api_key:
    st.warning("⚠️ Please enter your API key in the sidebar to begin.")
    st.markdown("### 🚀 Quick Start Guide")
    st.markdown("""
    1. Get your free API key from [Google AI Studio](https://aistudio.google.com/apikey)
    2. Enter it in the sidebar
    3. Upload an image or video file
    4. Click "Run Forensic Analysis"
    5. Review the AI's verdict and explanation
    """)
elif not uploaded_file:
    st.info("📤 Please upload an image or video file to analyze.")
    st.markdown("### 📁 Supported Formats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Images:**")
        st.markdown("- JPG/JPEG")
        st.markdown("- PNG")
    with col2:
        st.markdown("**Videos:**")
        st.markdown("- MP4")
        st.markdown("- MOV")
        st.markdown("- AVI")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>🔍 Powered by Ved Industries </p>
    <p>No data is stored or transmitted beyond the analysis session</p>
</div>
""", unsafe_allow_html=True)
