import cv2
import numpy as np

def draw_contours(original_img, change_map, min_area=500):
    """
    Improved visualization with overlay + boxes
    """

    # Convert grayscale → color
    output = cv2.cvtColor(original_img, cv2.COLOR_GRAY2BGR)

    # Create overlay (red mask)
    overlay = output.copy()
    overlay[change_map == 255] = [0, 0, 255]  # red

    # Blend original + overlay
    alpha = 0.4
    output = cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0)

    # Find contours
    contours, _ = cv2.findContours(
        change_map,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return output