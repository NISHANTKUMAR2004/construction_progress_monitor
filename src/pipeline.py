import cv2
from src.preprocessing import preprocess_image
from src.utils import load_image
from src.change_detection import detect_change
from src.visualization import draw_contours
from src.metrics import calculate_progress
from src.inference import predict_change

def process_pair(img1_path, img2_path):

    img1 = load_image(img1_path)
    img2 = load_image(img2_path)

    # Classical pipeline
    proc1 = preprocess_image(img1)
    proc2 = preprocess_image(img2)
    aligned2 = proc2
    change_map_cv, score = detect_change(proc1, aligned2)

    # 🔥 NEW: Deep Learning output
    change_map_dl = predict_change(img1, img2)

    # Visualization (use DL map for better results)
    highlighted = draw_contours(proc1, change_map_dl)

    # Progress
    progress = calculate_progress(change_map_dl)

    return proc1, aligned2, change_map_cv, change_map_dl, highlighted, score, progress