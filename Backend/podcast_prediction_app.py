from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib

# Load the model
try:
    model = joblib.load("mlartifacts/201757001456484594/cad5ba907960403f9e1ffde989808651/artifacts/model/model.pkl")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

app = FastAPI(title="Podcast Listening Time Predictor", version="1.0.0")

class PodcastFeatures(BaseModel):
    Podcast_Name: str
    Episode_Title: str
    Genre: str
    Publication_Day: str
    Publication_Time: str
    Guest_Popularity_percentage: float
    Host_Popularity_percentage: float

class PodcastPrediction(BaseModel):
    Predicted_Listening_Time: float

# Categorical encoding mappings
GENRE_MAPPING = {
    'Comedy': 0, 'Technology': 1, 'Health': 2, 'Education': 3, 
    'True Crime': 4, 'Business': 5, 'Sports': 6, 'News': 7,
    'Entertainment': 8, 'Science': 9, 'History': 10, 'Music': 11
}

PUBLICATION_DAY_MAPPING = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}

PUBLICATION_TIME_MAPPING = {
    'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3
}

@app.get("/")
def read_root():
    return {"message": "Podcast Listening Time Prediction API", "status": "running", "port": 5000}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PodcastPrediction)
def predict_listening_time(features: PodcastFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Encode categorical features
        genre_encoded = GENRE_MAPPING.get(features.Genre, 0)
        publication_day_encoded = PUBLICATION_DAY_MAPPING.get(features.Publication_Day, 0)
        publication_time_encoded = PUBLICATION_TIME_MAPPING.get(features.Publication_Time, 0)
        
        # Create input array with exactly 7 features in the correct order
        input_array = np.array([[
            0,  # Podcast_Name_encoded (placeholder)
            0,  # Episode_Title_encoded (placeholder)
            genre_encoded,
            publication_day_encoded,
            publication_time_encoded,
            features.Guest_Popularity_percentage,
            features.Host_Popularity_percentage
        ]])
        
        # Make prediction
        prediction = model.predict(input_array)
        predicted_time = float(prediction[0])
        
        return PodcastPrediction(Predicted_Listening_Time=predicted_time)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/example")
def get_example_request():
    """Get an example request format"""
    return {
        "example_request": {
            "Podcast_Name": "Tech Talk Today",
            "Episode_Title": "Episode 42",
            "Genre": "Technology",
            "Publication_Day": "Monday",
            "Publication_Time": "Morning",
            "Guest_Popularity_percentage": 68.8,
            "Host_Popularity_percentage": 75.2
        }
    }

@app.get("/model-info")
def get_model_info():
    """Get information about the API"""
    return {
        "model_loaded": model is not None,
        "required_features": [
            "Podcast_Name",
            "Episode_Title", 
            "Genre",
            "Publication_Day",
            "Publication_Time",
            "Guest_Popularity_percentage",
            "Host_Popularity_percentage"
        ],
        "categorical_options": {
            "Genre": list(GENRE_MAPPING.keys()),
            "Publication_Day": list(PUBLICATION_DAY_MAPPING.keys()),
            "Publication_Time": list(PUBLICATION_TIME_MAPPING.keys())
        },
        "model_expects": "7 features exactly"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server on http://127.0.0.1:5000")
    print("📖 API Documentation available at: http://127.0.0.1:5000/docs")
    uvicorn.run(app, host="127.0.0.1", port=5000)