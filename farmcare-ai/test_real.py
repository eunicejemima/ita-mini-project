import os
import io
from pathlib import Path
from backend.model.predict import predict_image

def test_real_images(dataset_path):
    crops_to_test = ["Tomato", "Potato", "Apple", "Grape", "Corn", "Strawberry"]
    
    # We will try to find folders matching these crops and states (healthy / diseased)
    # The folders in PlantVillage are usually named like "Tomato___healthy" or "Tomato___Early_blight"
    
    for crop in crops_to_test:
        print(f"\n--- Testing {crop} ---")
        
        # Find all directories for this crop
        crop_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d)) and crop.lower() in d.lower()]
        
        if not crop_dirs:
            print(f"No directories found for {crop}")
            continue
            
        healthy_dirs = [d for d in crop_dirs if 'healthy' in d.lower()]
        diseased_dirs = [d for d in crop_dirs if 'healthy' not in d.lower()]
        
        test_dirs = []
        if healthy_dirs:
            test_dirs.append(("Healthy", healthy_dirs[0]))
        if diseased_dirs:
            test_dirs.append(("Diseased", diseased_dirs[0]))
            
        for status, dname in test_dirs:
            dir_path = os.path.join(dataset_path, dname)
            images = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not images:
                print(f"No images in {dname}")
                continue
                
            img_path = os.path.join(dir_path, images[0])
            with open(img_path, 'rb') as f:
                img_bytes = f.read()
                
            pred_label, conf, top3 = predict_image(img_bytes, crop)
            print(f"Status: {status} | True Label: {dname}")
            print(f"  -> Predicted: {pred_label} (Confidence: {conf}%)")
            print(f"  -> Top 3: {top3}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_real_images(sys.argv[1])
    else:
        print("Please provide the path to the PlantVillage dataset.")
