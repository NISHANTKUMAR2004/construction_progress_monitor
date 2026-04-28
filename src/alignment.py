import cv2
import numpy as np

def align_images(img1, img2):
    """
    Align img2 to img1 using ORB + Homography (safe version)
    """

    # ORB detector
    orb = cv2.ORB_create(3000)

    # Detect keypoints
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # ❗ Safety check
    if des1 is None or des2 is None:
        print("Descriptors missing → skipping alignment")
        return img2

    # Match features
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)

    # Sort matches (best first)
    matches = sorted(matches, key=lambda x: x.distance)

    # 🔥 IMPORTANT FIX: reduce matches
    matches = matches[:50]

    # ❗ Safety check
    if len(matches) < 10:
        print("Not enough matches → skipping alignment")
        return img2

    # Extract points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])

    # 🔥 RANSAC Homography (robust)
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, 5.0)

    # ❗ Safety check
    if H is None:
        print("Homography failed → skipping alignment")
        return img2

    # Warp image
    h, w = img1.shape
    aligned = cv2.warpPerspective(img2, H, (w, h))

    return aligned