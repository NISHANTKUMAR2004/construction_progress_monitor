import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def detect_change(img1, img2):
    """
    Improved change detection with noise reduction
    """

    # SSIM
    score, diff = ssim(img1, img2, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY_INV)

    # 🔥 NEW: Morphological cleaning
    kernel = np.ones((5,5), np.uint8)

    # Remove noise
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Fill gaps
    cleaned = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    return cleaned, score