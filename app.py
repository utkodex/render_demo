import streamlit as st
import pickle
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="Placement Predictor", page_icon="🎓", layout="centered")

# --- MODEL LOADING ---
# We load the model directly in Streamlit now!
@st.cache_resource # This keeps the model in memory so it's fast
def load_model():
    model_path = 'model.pkl'
    with open(model_path, 'rb') as file:
        return pickle.load(file)

model = load_model()

# --- UI DESIGN ---
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
    # --- PREDICTION LOGIC ---
    # No more network requests! We do it right here.
    features = [iq, cgpa, tenth_marks, twelfth_marks, comm_skills]
    final_features = [np.array(features)]
    
    with st.spinner("Predicting..."):
        prediction = model.predict(final_features)
        output = 'Placed' if prediction[0] == 1 else 'Not Placed'
        
        # Display result
        if output == "Placed":
            st.success(f"### Prediction: **{output}** 🎉")
            st.balloons()
        else:
            st.error(f"### Prediction: **{output}** ❌")
