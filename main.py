import os
import matplotlib.pyplot as plt
from src.utils import get_image_pairs
from src.pipeline import process_pair

base_path = "data/raw/LEVIR-CD/train"
t1_path = os.path.join(base_path, "A")
t2_path = os.path.join(base_path, "B")

pairs = get_image_pairs(t1_path, t2_path)

img1, img2, change_cv, change_dl, highlighted, score, progress = process_pair(
    pairs[0][0], pairs[0][1]
)

print(f"SSIM Score: {score:.4f}")
print(f"DL Progress: {progress:.2f}%")

plt.figure(figsize=(18,5))

plt.subplot(1,5,1)
plt.imshow(img1, cmap='gray')
plt.title("t1")

plt.subplot(1,5,2)
plt.imshow(img2, cmap='gray')
plt.title("Aligned t2")

plt.subplot(1,5,3)
plt.imshow(change_cv, cmap='gray')
plt.title("CV Change")

plt.subplot(1,5,4)
plt.imshow(change_dl, cmap='gray')
plt.title("DL Change")

plt.subplot(1,5,5)
plt.imshow(highlighted)
plt.title(f"Progress: {progress:.2f}%")

plt.show()