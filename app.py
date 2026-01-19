import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Gemini Forensic AI", page_icon="🔍", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #00c6ff, #0072ff); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Deepfake AI Video & Image Detector")
st.write("Upload a file to analyze its authenticity using **Gemini 3 Flash** reasoning.")

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
    <p>🔍 Powered by Google Gemini 3 Flash • Built with Streamlit</p>
    <p>No data is stored or transmitted beyond the analysis session</p>
</div>
""", unsafe_allow_html=True)
