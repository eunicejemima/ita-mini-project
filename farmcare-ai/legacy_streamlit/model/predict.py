import json
import os
import random
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'class_names.json')

with open(CLASS_NAMES_PATH, 'r') as f:
    CLASS_NAMES = json.load(f)

MODEL_LOADED = False

def load_model():
    global MODEL_LOADED
    MODEL_LOADED = True
    return True

def predict_image(image_bytes, selected_crop):
    """
    DEMO mode prediction.
    """
    if not MODEL_LOADED:
        load_model()
        
    time.sleep(1.5)
    
    possible_classes = CLASS_NAMES.get(selected_crop, ["Healthy"])
    predicted_class = random.choice(possible_classes)
    confidence = random.uniform(40.0, 98.0)
    
    return predicted_class, round(confidence, 1)
