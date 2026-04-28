import torch
import cv2
import numpy as np
import os
from pathlib import Path
from src.model import SiameseChangeDetector

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    """
    Load and cache the model for Streamlit deployment.
    Returns the model in eval mode on the appropriate device.
    """
    try:
        model = SiameseChangeDetector().to(device)
        
        # Get the absolute path to model.pth relative to project root
        # Using pathlib for better cross-platform compatibility
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        model_path = project_root / "model.pth"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        model.load_state_dict(torch.load(str(model_path), map_location=device))
        model.eval()
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

# Load model once at startup
try:
    model = load_model()
except RuntimeError as e:
    print(f"Warning: {e}")
    model = None


def preprocess_dl(image):
    """Preprocess image for model inference."""
    try:
        if image is None or image.size == 0:
            raise ValueError("Invalid image provided")
        
        image = cv2.resize(image, (256, 256))

        # SAME normalization as training
        image = (image / 255.0 - 0.5) / 0.5

        image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)
        image = image.unsqueeze(0)

        return image.to(device)
    except Exception as e:
        raise RuntimeError(f"Image preprocessing failed: {str(e)}")


def predict_change(img1, img2):
    """Predict changes between two images using the model."""
    
    if model is None:
        raise RuntimeError("Model not loaded. Check if model.pth exists.")
    
    try:
        img1 = preprocess_dl(img1)
        img2 = preprocess_dl(img2)

        with torch.no_grad():
            output = model(img1, img2)

            output = torch.nn.functional.interpolate(
                output, size=(512, 512), mode='bilinear'
            )

            # Apply sigmoid here
            output = torch.sigmoid(output)

            output = output.squeeze().cpu().numpy()

        change_map = (output > 0.3).astype(np.uint8) * 255

        return change_map
    except Exception as e:
        raise RuntimeError(f"Model inference failed: {str(e)}")