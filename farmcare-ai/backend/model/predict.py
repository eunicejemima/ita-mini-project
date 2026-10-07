import json
import random
import time
import io
import os
from pathlib import Path
from PIL import Image
import numpy as np

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

BASE_DIR = Path(__file__).parent
CLASS_NAMES_PATH = BASE_DIR / 'class_names.json'
MODEL_PATH = BASE_DIR / 'farmcare_model.keras'

with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = json.load(f)

MODEL = None
MODEL_LOADED = False

def load_model():
    global MODEL, MODEL_LOADED
    if not MODEL_LOADED and MODEL_PATH.exists():
        MODEL = tf.keras.models.load_model(str(MODEL_PATH))
        MODEL_LOADED = True
    return MODEL_LOADED

def is_demo_mode():
    return not load_model()

def predict_image(image_bytes, selected_crop):
    if is_demo_mode():
        time.sleep(1.5)
        # Basic filtering for demo mode based on crop
        possible = [c for c in CLASS_NAMES if c["crop"].lower().replace(' ', '') in selected_crop.lower().replace('_', '') or selected_crop.lower().replace('_', '') in c["crop"].lower().replace(' ', '')]
        if not possible:
            possible = CLASS_NAMES
        predicted_class = random.choice(possible)["label"]
        confidence = random.uniform(40.0, 98.0)
        return predicted_class, round(confidence, 1), []
    
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = MODEL.predict(img_array)
        probs = predictions[0]
        confidence = 100 * float(np.max(probs))
        predicted_idx = int(np.argmax(probs))
        
        predicted_label = CLASS_NAMES[predicted_idx]["label"]
        
        # Get top 3 (actually top 3 total, so next 2, or top 3 other possibilities?)
        # "top 3 predictions with confidences... Other possibilities ... Early Blight 91%, Late Blight 6%, Healthy 2%"
        top_indices = np.argsort(probs)[::-1][:3]
        top_3 = []
        for idx in top_indices:
            lbl = CLASS_NAMES[int(idx)]["label"]
            conf = round(100 * float(probs[int(idx)]), 1)
            top_3.append({"label": lbl, "confidence": conf})
            
        return predicted_label, round(float(confidence), 1), top_3
    except Exception as e:
        print(f"Error predicting image: {e}")
        raise e
