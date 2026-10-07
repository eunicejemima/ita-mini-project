import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = BASE_DIR / 'knowledge_base.json'
CLASS_NAMES_PATH = BASE_DIR.parent / 'model' / 'class_names.json'

with open(KNOWLEDGE_BASE_PATH, 'r') as f:
    knowledge_base = json.load(f)

with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)

def get_class_info(prediction_label):
    for c in class_names:
        if c["label"] == prediction_label:
            return c
    return {"crop": "Unknown", "condition": "Unknown", "label": prediction_label, "type": "healthy"}

def generate_action_plan(crop, prediction_label, confidence, rain_recency, soil_condition, problem_duration):
    class_info = get_class_info(prediction_label)
    disease_type = class_info.get("type", "healthy")
    
    if disease_type == "healthy":
        status_level = "Healthy"
    elif confidence < 60 or problem_duration == "More than a week":
        status_level = "Urgent Attention"
    else:
        status_level = "Attention Recommended"

    kb_info = knowledge_base.get(prediction_label)
    if not kb_info:
        # fallback
        kb_info = {
            "description": "Unknown condition.",
            "things_to_inspect": ["Monitor crop closely."],
            "monitor_signs": ["Check for spread."],
            "general_actions": ["Consult an expert."],
            "expert_help": "Seek professional guidance."
        }

    actions = list(kb_info.get("general_actions", []))
    
    if soil_condition == "Dry" and rain_recency not in ["Today", "1–3 days ago"]:
        actions.append("Review watering schedule; ensure the plant is not under drought stress.")
    if disease_type != "healthy" and (rain_recency in ["Today", "1–3 days ago"] or soil_condition == "Wet"):
        actions.append("Avoid overhead watering, as wet leaves favor disease spread.")

    expert_help = kb_info.get("expert_help", "Consult a local agricultural expert for confirmation.")
    if status_level == "Urgent Attention" and disease_type != "healthy":
        expert_help = "Due to the duration or uncertainty, we strongly recommend consulting a local agricultural expert IMMEDIATELY for confirmation."

    monitor_signs = kb_info.get("monitor_signs", [])
    if isinstance(monitor_signs, list):
        monitor_signs = " ".join(monitor_signs)

    things_to_inspect = kb_info.get("things_to_inspect", [])
    if isinstance(things_to_inspect, list):
        things_to_inspect = " ".join(things_to_inspect)

    description = kb_info.get("description", "")
    pred_crop_clean = class_info.get("crop", "").lower().replace(" ", "").replace("_", "")
    sel_crop_clean = crop.lower().replace(" ", "").replace("_", "")
    if pred_crop_clean and sel_crop_clean and pred_crop_clean != sel_crop_clean:
        description = f"⚠️ WARNING: You selected {crop.replace('_', ' ')} but the AI recognized this as {class_info.get('crop')}. Showing results for {class_info.get('crop')}. " + description

    return {
        "status_level": status_level,
        "actions": actions,
        "monitor_signs": monitor_signs,
        "things_to_inspect": things_to_inspect,
        "expert_help": expert_help,
        "description": description
    }
