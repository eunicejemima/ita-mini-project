# 🌱 FarmCare AI

**AI-Powered Crop Health & Context-Aware Action Recommendation System**

> FarmCare AI lets a farmer upload a photo of a crop leaf. A deep learning model identifies the *possible* crop health problem, and the system combines that result with simple answers from the farmer to produce a personalized action plan.

*ITA Mini Project*

---

## 📌 Problem Statement

A farmer may notice spots or discoloration on a leaf but may not know what the problem could be, whether it is serious, what to check next, or whether nearby plants are at risk. Many existing crop-disease apps stop at **image → disease name**.

FarmCare AI goes one step further:

```
📷 SEE  →  🤖 UNDERSTAND  →  🌱 ACT
```

1. **See:** the farmer selects a crop and uploads a leaf photo.
2. **Understand:** an AI model predicts the possible condition with a confidence score.
3. **Act:** the app asks three simple questions (recent rain, soil condition, how long the problem has been present) and generates a context-aware action plan, signs to monitor, and advice on when to consult an expert.

---

## ✨ Features

- Image-based crop health analysis for **14 crops / 38 classes** (healthy and diseased)
- Confidence score and top-3 "other possibilities"
- Context-aware action plan based on disease category and the farmer's answers
- Safety checks: low-confidence warning and crop-mismatch warning
- "Monitor these signs" and "When to get expert help" guidance
- Saved crop profile and history of previous checks
- Crop Guide with growth stages, things to monitor, and common issues
- Safe by design: **no pesticide names, chemicals, or dosages** are ever recommended

---

## 🧠 How the AI Works

| Item | Details |
|---|---|
| Task | Image classification (38 classes) |
| Model | **MobileNetV2** (CNN) with transfer learning |
| Pre-trained on | ImageNet |
| Fine-tuned on | PlantVillage dataset |
| Input | 224 × 224 RGB leaf image |
| Output | Probability for each of the 38 classes |
| Framework | TensorFlow / Keras |
| Training | Google Colab (GPU) |
| Result | **96.3% validation accuracy** |

**Training summary**

- Dataset split: 80% training (43,444 images) and 20% validation (10,861 images)
- Data augmentation: random flip, rotation, and zoom
- Phase 1: frozen MobileNetV2 base, new classification head (8 epochs)
- Phase 2: fine-tuning the top 30 layers with a low learning rate (4 epochs)

**Where the AI runs in the code:** `backend/model/predict.py` loads `farmcare_model.keras` and calls `MODEL.predict(...)` on the uploaded image.

**The action plan is not AI.** The context engine (`backend/engine/context_engine.py`) is a rule-based system that classifies each condition as fungal, bacterial, viral, pest, or healthy, and then adjusts safe general advice using the farmer's answers.

---

## 🏗️ System Flow

```
Farmer selects crop + uploads leaf photo
              ↓
   AI model (MobileNetV2 CNN) → possible condition + confidence
              ↓
   Safety checks (low confidence? wrong crop?)
              ↓
   Farmer answers 3 simple questions (rain, soil, duration)
              ↓
   Context engine (rule-based) → action plan
              ↓
   Report: result, actions, monitor signs, expert-help advice
              ↓
   Saved to history
```

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI:** TensorFlow / Keras, MobileNetV2, NumPy, Pillow
- **Frontend:** HTML, CSS, JavaScript (single-page app with hash routing)
- **Storage:** local JSON / CSV files (no database)
- **Dataset:** PlantVillage (Kaggle)

---

## 📁 Project Structure

```
farmcare-ai/
├── backend/
│   ├── main.py                  # FastAPI app and API endpoints
│   ├── model/
│   │   ├── predict.py           # loads the model and predicts (AI part)
│   │   ├── train.py             # training script
│   │   ├── farmcare_model.keras # trained MobileNetV2 model
│   │   ├── class_names.json     # crop / condition / label mapping
│   │   └── class_names_raw.json # class order used during training
│   └── engine/
│       ├── context_engine.py    # rule-based action plan generator
│       └── knowledge_base.json  # per-condition guidance
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/                      # app, router, API, and UI components
├── legacy_streamlit/            # earlier Streamlit prototype (not used)
├── screenshots/
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

**Requirements:** Python 3.10 or newer, and pip.

1. **Open a terminal in the project root** (the folder that contains `backend/` and `frontend/`):

   ```bash
   cd farmcare-ai
   ```

2. **(Recommended) Create a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Check that the model file exists:** `backend/model/farmcare_model.keras`

5. **Start the server** (run this from the project root)

   ```bash
   python -m uvicorn backend.main:app --port 8000
   ```

   Wait for `Application startup complete` (the first start takes longer while TensorFlow loads).

6. **Open the app:** <http://127.0.0.1:8000>

   API docs (auto-generated by FastAPI): <http://127.0.0.1:8000/docs>

**Troubleshooting**

- `No module named 'backend'` means you are not in the project root.
- `address already in use` means another server is on that port. Use `--port 8010` and open `http://127.0.0.1:8010`.
- If the model file is missing, the app falls back to demo mode with simulated predictions.

---

## 🧪 How to Use

1. Open **AI Crop Check** and select the crop.
2. Upload a clear photo of a single leaf.
3. Answer the three questions (recent rain, soil, how long you have noticed the problem).
4. Click **Analyze** to see the result, confidence, action plan, and signs to monitor.
5. Open **My Report** to see the full report and past checks.

Tip: for testing, use images from the PlantVillage `color` folder. Photos with soil, hands, or many leaves may score lower.

---

## 📊 Dataset

**PlantVillage** (Kaggle: `abdallahalidev/plantvillage-dataset`): 54,305 labeled leaf images, 38 classes, 14 crops (Apple, Blueberry, Cherry, Corn/Maize, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato).

> Hughes, D. P., & Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.*

The dataset is not included in this repository. Please check the license on the dataset page before reuse.

---

## ⚠️ Limitations

- PlantVillage images are single leaves on plain backgrounds, so accuracy on real field photos will be lower than the reported 96.3%.
- The 96.3% was measured on held-out images from the same dataset, not on farm photos.
- Recommendation rules are general and have not been validated by agricultural experts.
- Only the 38 classes in the dataset are supported (for example, rice is not included).
- Results are **possible indications only**, not a confirmed diagnosis.

---

## 🔮 Future Scope

- Retrain with real field images collected from farms
- Regional language and voice support
- Weather integration and a mobile app
- Expert-validated recommendation rules
- Visual explanations of which leaf regions influenced the prediction

---

## 🛡️ Disclaimer

FarmCare AI gives possible indications for guidance only. It does not recommend pesticides or dosages. Always consult a local agricultural expert for confirmation and treatment advice.

---
