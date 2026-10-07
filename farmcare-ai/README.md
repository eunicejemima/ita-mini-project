# FarmCare AI

A context-aware AI farm action planner. 

## Requirements
Python 3.10+

## Setup & Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the FastAPI backend:
   `uvicorn backend.main:app --reload`
3. Access the web interface at:
   `http://localhost:8000`

## Model Training (Optional)
Dataset required: PlantVillage
1. Place dataset in `data/PlantVillage/`
2. Run `python backend/model/train.py`
3. The model `farmcare_model.keras` will be generated in `backend/model/`. 
   Once this file exists, the app automatically switches from DEMO MODE to REAL MODE.
