import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup the AI
genai.configure(api_key="YOUR_GOOGLE_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📸 My Free AI Scout")

# 2. The Camera Input
img_file = st.camera_input("Take a photo of something!")

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Captured Image")
    
    # 3. Ask the AI to look at the photo
    response = model.generate_content(["Describe what you see in this photo briefly.", img])
    
    st.subheader("The AI Says:")
    st.write(response.text)
