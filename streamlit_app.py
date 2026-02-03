import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="CoachAI", page_icon="🎤")
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 1. Securely get the API Key from Streamlit Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Update your model definition at the top of the script
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=(
        "You are an expert Communication Coach. Analyze videos for: "
        "1. Body Language (posture, gestures, eye contact). "
        "2. Vocal Delivery (tone, pacing, filler words). "
        "3. Content (clarity, structure). "
        "Provide constructive feedback in a bulleted list with 'Strengths' and 'Areas for Improvement'."
    )
)

st.title("📸 AI Vision & Video Bot")

# Use tabs to keep the UI clean
tab1, tab2 = st.tabs(["Photo Mode", "Video Mode"])

with tab1:
    img_file = st.camera_input("Snap a photo")
    if img_file:
        st.image(img_file)
        with st.spinner("AI is thinking..."):
            response = model.generate_content(["Describe this image.", img_file])
            st.write(response.text)

with tab2:
    # Most mobile browsers allow you to record video directly when you click 'Browse'
   with tab2:
    video_file = st.file_uploader("Record your speech", type=['mp4', 'mov', 'avi'])
    
    if video_file:
        st.video(video_file)
        
        # Add feedback options
        feedback_type = st.radio(
            "What should I focus on?",
            ["General Critique", "Interview Readiness", "Public Speaking/Confidence"]
        )

        if st.button("Analyze My Communication"):
            with st.spinner("Reviewing your performance..."):
                user_video = genai.upload_file(video_file)
                
                # Wait for processing
                while user_video.state.name == "PROCESSING":
                    time.sleep(2)
                    user_video = genai.get_file(user_video.name)

                # Send specific instructions based on the button selected
                prompt = f"Analyze this video for {feedback_type}. Provide specific timestamps if possible."
                response = model.generate_content([user_video, prompt])
                
                st.markdown("### 📊 Your Coach's Feedback")
                st.write(response.text)
