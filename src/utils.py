import cv2
import os

def load_image(path):
    return cv2.imread(path)

def get_image_pairs(t1_path, t2_path):
    t1_images = sorted(os.listdir(t1_path))
    t2_images = sorted(os.listdir(t2_path))

    pairs = []
    for img_name in t1_images:
        pairs.append((
            os.path.join(t1_path, img_name),
            os.path.join(t2_path, img_name)
        ))
    
    return pairs