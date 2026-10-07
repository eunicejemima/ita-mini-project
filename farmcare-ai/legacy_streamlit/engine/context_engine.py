import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, 'engine', 'knowledge_base.json')

with open(KNOWLEDGE_BASE_PATH, 'r') as f:
    knowledge_base = json.load(f)

def generate_action_plan(crop, disease, confidence, rain_recency, soil_condition, problem_duration):
    """
    Generate an action plan based on AI prediction and context.
    """
    if disease == "Healthy":
        status_level = "Healthy"
    elif confidence < 60 or problem_duration == "More than a week":
        status_level = "Urgent Attention"
    else:
        status_level = "Attention Recommended"

    actions = []
    
    if disease == "Healthy":
        actions.append("Maintain your current care routine.")
        if soil_condition == "Dry":
            actions.append("Review watering schedule as the soil appears dry.")
        actions.append("Continue routine monitoring of your crop.")
    else:
        if "Blight" in disease or "Rust" in disease or "Mold" in disease:
            actions.append("Inspect nearby plants to see if the issue is spreading.")
            if rain_recency in ["Today", "1–3 days ago"] or soil_condition == "Wet":
                actions.append("Ensure good air circulation, as wet conditions favor fungal spread.")
            actions.append("Carefully remove and isolate severely affected leaves if feasible.")
        elif disease == "Bacterial Spot":
            actions.append("Inspect nearby plants for similar spots.")
            actions.append("Avoid overhead watering to prevent splashing.")
            if soil_condition == "Wet":
                actions.append("Review drainage to prevent standing water.")
        else:
            actions.append("Isolate the affected area if possible.")
            actions.append("Check neighboring plants.")

        if soil_condition == "Dry" and rain_recency not in ["Today", "1–3 days ago"]:
            actions.append("Review watering schedule; ensure the plant is not under drought stress.")

    crop_kb = knowledge_base.get(crop, {})
    disease_kb = crop_kb.get(disease, {})
    monitor_signs = disease_kb.get("monitor_signs", "Watch for any changes in leaf color or texture.")
    
    if disease != "Healthy":
        if status_level == "Urgent Attention":
            expert_help = "Due to the duration or uncertainty, we strongly recommend consulting a local agricultural expert immediately for confirmation and safe treatment options."
        else:
            expert_help = "Consult a local agricultural expert to confirm this indication and get safe advice."
    else:
        expert_help = "Consult a local expert if you notice any unusual symptoms later."

    return {
        "status_level": status_level,
        "actions": actions,
        "monitor_signs": monitor_signs,
        "expert_help": expert_help
    }
