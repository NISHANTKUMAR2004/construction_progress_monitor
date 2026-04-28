import torch
import cv2
import numpy as np
import os
from src.model import SiameseChangeDetector

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SiameseChangeDetector().to(device)
# Get the absolute path to model.pth relative to project root
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model.pth")
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()


def preprocess_dl(image):
    image = cv2.resize(image, (256, 256))

    # SAME normalization as training
    image = (image / 255.0 - 0.5) / 0.5

    image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)
    image = image.unsqueeze(0)

    return image.to(device)


def predict_change(img1, img2):

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