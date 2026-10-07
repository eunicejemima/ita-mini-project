import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.engine.context_engine import generate_action_plan
from backend.model.predict import predict_image, is_demo_mode

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
MY_CROP_FILE = DATA_DIR / "my_crop.json"
HISTORY_FILE = DATA_DIR / "check_history.csv"

class MyCropModel(BaseModel):
    crop: str
    age: int
    recent_rain: str
    soil: str

@app.get("/api/my-crop")
def get_my_crop():
    if MY_CROP_FILE.exists():
        with open(MY_CROP_FILE, 'r') as f:
            return json.load(f)
    return {"crop": "", "age": 30, "recent_rain": "", "soil": ""}

@app.post("/api/my-crop")
def save_my_crop(data: MyCropModel):
    with open(MY_CROP_FILE, 'w') as f:
        json.dump(data.model_dump(), f)
    return {"status": "success"}

@app.post("/api/analyze")
async def analyze_crop(
    crop: str = Form(...),
    rain: str = Form(...),
    soil: str = Form(...),
    duration: str = Form(...),
    file: UploadFile = File(...)
):
    image_bytes = await file.read()
    
    prediction_label, confidence, top_3 = predict_image(image_bytes, crop)
    plan = generate_action_plan(crop, prediction_label, confidence, rain, soil, duration)
    
    file_exists = HISTORY_FILE.exists()
    history_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "crop": crop,
        "prediction": prediction_label,
        "confidence": confidence,
        "rain": rain,
        "soil": soil,
        "duration": duration
    }
    df = pd.DataFrame([history_data])
    df.to_csv(HISTORY_FILE, mode='a', header=not file_exists, index=False)
    
    return {
        "crop": crop,
        "prediction": prediction_label,
        "confidence": confidence,
        "status": plan["status_level"],
        "actions": plan["actions"],
        "monitor_signs": plan["monitor_signs"],
        "things_to_inspect": plan["things_to_inspect"],
        "expert_help": plan["expert_help"],
        "description": plan["description"],
        "is_demo": is_demo_mode(),
        "top_3": top_3,
        "timestamp": history_data["timestamp"]
    }

@app.get("/api/history")
def get_history():
    if HISTORY_FILE.exists():
        df = pd.read_csv(HISTORY_FILE)
        return df.to_dict(orient="records")
    return []

@app.get("/api/crops")
def get_crops():
    from backend.engine.context_engine import class_names
    unique_crops = sorted(list(set(c["crop"] for c in class_names)))
    return unique_crops

frontend_dir = BASE_DIR.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
