import torch
import torch.nn as nn

class SiameseChangeDetector(nn.Module):
    def __init__(self):
        super(SiameseChangeDetector, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        # Decoder (NO sigmoid here)
        self.decoder = nn.Sequential(
            nn.Conv2d(32, 16, 3, padding=1),
            nn.ReLU(),

            nn.Conv2d(16, 1, 1)
        )

    def forward(self, img1, img2):
        f1 = self.encoder(img1)
        f2 = self.encoder(img2)

        diff = torch.abs(f1 - f2)

        out = self.decoder(diff)

        return out