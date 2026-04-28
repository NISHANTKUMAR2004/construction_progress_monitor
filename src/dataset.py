import os
import cv2
import torch
import random
from torch.utils.data import Dataset

class ChangeDetectionDataset(Dataset):
    def __init__(self, base_path):
        self.path_A = os.path.join(base_path, "A")
        self.path_B = os.path.join(base_path, "B")
        self.path_label = os.path.join(base_path, "label")

        self.images = sorted(os.listdir(self.path_A))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        name = self.images[idx]

        img1 = cv2.imread(os.path.join(self.path_A, name))
        img2 = cv2.imread(os.path.join(self.path_B, name))
        label = cv2.imread(os.path.join(self.path_label, name), 0)

        # Resize
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))
        label = cv2.resize(label, (256, 256))

        # Data Augmentation
        if random.random() > 0.5:
            img1 = cv2.flip(img1, 1)
            img2 = cv2.flip(img2, 1)
            label = cv2.flip(label, 1)

        # Normalize (IMPORTANT)
        img1 = (img1 / 255.0 - 0.5) / 0.5
        img2 = (img2 / 255.0 - 0.5) / 0.5

        label = label / 255.0  # 0 or 1

        # To tensor
        img1 = torch.tensor(img1, dtype=torch.float32).permute(2, 0, 1)
        img2 = torch.tensor(img2, dtype=torch.float32).permute(2, 0, 1)
        label = torch.tensor(label, dtype=torch.float32).unsqueeze(0)

        return img1, img2, label