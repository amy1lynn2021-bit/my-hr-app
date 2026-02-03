import streamlit as st
import google.generativeai as genai
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

if video_file:
    st.video(video_file)
    
    # Optional selection for focus
    focus = st.selectbox("What should I look for?", ["General Feedback", "Confidence", "Reducing Filler Words"])

    if st.button("Get Coaching Feedback"):
        with st.status("Coach is watching your video...", expanded=True) as status:
            st.write("Uploading to AI brain...")
            user_video = genai.upload_file(video_file)
            
            # Polling to check if the video is ready
            while user_video.state.name == "PROCESSING":
                time.sleep(2)
                user_video = genai.get_file(user_video.name)
            
            st.write("Analyzing your communication style...")
            prompt = f"Please analyze this video for {focus}. Provide a structured critique."
            response = model.generate_content([user_video, prompt])
            
            status.update(label="Analysis Complete!", state="complete")
        
        st.subheader("📊 Coach's Report")
        st.markdown(response.text)
