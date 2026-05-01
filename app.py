import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(page_title="Placement Predictor", page_icon="🎓", layout="centered")

# Backend URL
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://127.0.0.1:8000")

st.title("🎓 Student Placement Prediction")
st.markdown("Enter the student details below to predict placement status.")

# Form for user input
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        iq = st.number_input("IQ Score", min_value=0, max_value=200, value=100)
        tenth_marks = st.number_input("10th Marks (%)", min_value=0, max_value=100, value=75)
        comm_skills = st.slider("Communication Skills", 0.0, 10.0, 5.0, 0.1)

    with col2:
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.01)
        twelfth_marks = st.number_input("12th Marks (%)", min_value=0, max_value=100, value=75)

    submit_button = st.form_submit_button(label="Predict Placement")

if submit_button:
    # Prepare data for API
    payload = {
        "IQ": iq,
        "CGPA": cgpa,
        "10th_Marks": tenth_marks,
        "12th_Marks": twelfth_marks,
        "Communication_Skills": comm_skills
    }
    
    with st.spinner("Talking to FastAPI Backend..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/predict_api", json=payload)
            response.raise_for_status()
            result = response.json()
            prediction = result.get("prediction")
            
            # Display result with nice styling
            if prediction == "Placed":
                st.success(f"### Prediction: **{prediction}** 🎉")
                st.balloons()
            else:
                st.error(f"### Prediction: **{prediction}** ❌")
                
        except Exception as e:
            st.warning(f"Could not connect to Backend: {e}")
