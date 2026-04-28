import cv2
from src.preprocessing import preprocess_image
from src.utils import load_image
from src.change_detection import detect_change
from src.visualization import draw_contours
from src.metrics import calculate_progress
from src.inference import predict_change

def process_pair(img1_path, img2_path):
    """
    Process a pair of images for change detection.
    
    Args:
        img1_path: Path to the first image (before)
        img2_path: Path to the second image (after)
    
    Returns:
        Tuple of (proc1, aligned2, change_map_cv, change_map_dl, highlighted, score, progress)
    
    Raises:
        RuntimeError: If image processing fails
    """
    try:
        img1 = load_image(img1_path)
        img2 = load_image(img2_path)
        
        if img1 is None or img2 is None:
            raise ValueError("Failed to load one or both images")

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
    except Exception as e:
        raise RuntimeError(f"Pipeline processing failed: {str(e)}")