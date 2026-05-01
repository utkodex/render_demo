from fastapi import FastAPI, Body
import pickle
import numpy as np
import uvicorn
import os

app = FastAPI()

# Load the trained model
model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.get("/")
async def health_check():
    return {"status": "FastAPI Backend is running"}

@app.post("/predict_api")
async def predict_api(data: dict = Body(...)):
    # Extract features from JSON payload
    features = [
        data.get("IQ"),
        data.get("CGPA"),
        data.get("10th_Marks"),
        data.get("12th_Marks"),
        data.get("Communication_Skills")
    ]
    
    # Convert to numpy array for prediction
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    output = 'Placed' if prediction[0] == 1 else 'Not Placed'
    
    return {"prediction": output}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
