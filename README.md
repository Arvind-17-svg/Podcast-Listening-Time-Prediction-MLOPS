# Podcast-Listening-Time-Prediction-MLOPS

In this Project, The Podcast Listening Time in Minutes is predicted using LightGBM Model. To enable better model versioning and tracking MLFlow is used respectively. 

For Inference Purposes, FastAPI Backend is Connected to Streamlit Frontend and Dockerized using docker compose.

To Run the Dockerized Version, Following steps are to be followed.

Step 1) Clone the Repository
git clone

Step 2 ) Make sure Docker Desktop is Installed.

Step 3 ) Use the below commands to dockerise and run 
docker compose up --build

File Structure
Artifacts - MLFlow Artifacts (Pickle File).
Backend - FastAPI Backend
Frontend - Streamlit Frontend.
Podcast-Prediction-ML - ML Model for Podcast Prediction
