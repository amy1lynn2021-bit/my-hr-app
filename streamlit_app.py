import streamlit as st
import google.generativeai as genai
import time

# 1. Securely get the API Key from Streamlit Secrets
genai.configure(api_key=st.secrets["AIzaSyAsYBpqydoFBF6IT-IaRsWdGK-JlyVuw5k"])
model = genai.GenerativeModel('gemini-1.5-flash')

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
    video_file = st.file_uploader("Record or upload a short video", type=['mp4', 'mov', 'avi'])
    
    if video_file:
        st.video(video_file)
        if st.button("Analyze Video"):
            with st.spinner("Processing video (this takes a moment)..."):
                # Upload to Google's temporary storage
                # Note: In a production app, you'd manage these files, 
                # but for a hobby project, this works!
                user_video = genai.upload_file(video_file)
                
                # Wait for the AI to "watch" the video
                while user_video.state.name == "PROCESSING":
                    time.sleep(2)
                    user_video = genai.get_file(user_video.name)

                response = model.generate_content([user_video, "Summarize what happens in this video."])
                st.write(response.text)
