# app.py (Flask Frontend)

from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# The URL of the FastAPI backend
# Locally it's 8000, on Render we use an environment variable
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://127.0.0.1:8000")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Get data from the Flask Form
    form_data = {
        "IQ": int(request.form.get("IQ")),
        "CGPA": float(request.form.get("CGPA")),
        "10th_Marks": int(request.form.get("10th_Marks")),
        "12th_Marks": int(request.form.get("12th_Marks")),
        "Communication_Skills": float(request.form.get("Communication_Skills"))
    }
    
    try:
        # 2. Forward the data to the FastAPI Backend
        response = requests.post(f"{FASTAPI_URL}/predict_api", json=form_data)
        response.raise_for_status() # Check for errors
        
        # 3. Get the prediction result
        result = response.json()
        output = result.get("prediction", "Error")
        
    except Exception as e:
        output = f"Connection Error: {str(e)}"

    return render_template('index.html', prediction_text='Prediction: {}'.format(output))

if __name__ == "__main__":
    # Flask runs on 5000 by default
    app.run(port=5000, debug=True)
