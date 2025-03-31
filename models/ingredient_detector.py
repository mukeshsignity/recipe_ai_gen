import os
import torch
import cv2
import numpy as np
from ultralytics import YOLO

MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "best.pt"))

class IngredientDetector:
    def __init__(self):
        """Load trained YOLOv8 model for ingredient detection."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

        self.model = YOLO(MODEL_PATH).to(self.device)
        print(f"✅ Model loaded from {MODEL_PATH} on {self.device}")

    def detect_ingredients(self, image_bytes):
        """Detect ingredients from an uploaded image."""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Invalid image data. Could not decode.")

            results = self.model(image)

            detected_ingredients = set()  # Use a set to avoid duplicates
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        name = result.names.get(cls, "Unknown")
                        detected_ingredients.add(name.lower())  # Store lowercase for consistency

            return list(detected_ingredients)

        except Exception as e:
            print(f"❌ Error during detection: {e}")
            return []
