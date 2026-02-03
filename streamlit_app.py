import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# 1. Page Configuration (Must be first!)
st.set_page_config(page_title="CoachAI", page_icon="🎤")

# 2. Styling
st.markdown("""
    <style>
    .stHeader { background-color: #f8f9fa; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. AI Setup
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=(
        "You are an elite Communication Coach. Your goal is to analyze video clips and "
        "provide a breakdown of: 1. Vocal Pacing, 2. Body Language, 3. Narrative Clarity. "
        "Be encouraging but precise. Always give a 'Top Strength' and a 'Key Focus Area'."
    )
)

st.title("🎤 CoachAI: Video Feedback")
st.info("Record a 10-20 second clip of yourself speaking to get instant feedback.")

# 4. Video Input
# On mobile, clicking this allows the user to 'Take Video' immediately.
video_file = st.file_uploader("Upload or Record Video", type=['mp4', 'mov', 'avi'])

video_file = st.file_uploader("Upload or Record Video", type=['mp4', 'mov'])

if video_file is not None:
    # 1. Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(video_file.read())
        temp_path = tmp_file.name

    try:
        # 2. Upload to Google
        st.info("Sending video to Gemini...")
        user_video = genai.upload_file(path=temp_path)
        
        # 3. THE WAIT LOOP: Check status until it's ACTIVE
        with st.spinner("AI is analyzing the video frames..."):
            while user_video.state.name == "PROCESSING":
                time.sleep(3) # Check every 3 seconds
                user_video = genai.get_file(user_video.name)
            
            if user_video.state.name == "FAILED":
                st.error("Video processing failed on Google's side.")
                st.stop()

        st.success("Video ready for coaching!")

        # 4. Now you can safely call generate_content
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([user_video, "Analyze this video for me."])
        st.write(response.text)

    finally:
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
  
