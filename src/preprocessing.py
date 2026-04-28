import cv2

def preprocess_image(image, size=(512, 512)):
    """
    Preprocess the input image:
    1. Resize
    2. Convert to grayscale
    3. Apply Gaussian blur (noise removal)
    """

    # Step 1: Resize image
    image_resized = cv2.resize(image, size)

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

    # Step 3: Noise removal using Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred