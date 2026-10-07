import numpy as np
from PIL import Image
import io
import asyncio
from backend.model.predict import predict_image

crops = ["Tomato", "Potato", "Apple", "Grape", "Corn", "Strawberry"]
results = []

for crop in crops:
    # generate a random noise image 224x224
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    img_bytes = buf.getvalue()
    
    label, conf = predict_image(img_bytes, crop)
    results.append(f"Crop: {crop} => Predicted: {label} (Confidence: {conf}%)")

print("Test Predictions:")
for r in results:
    print(r)
