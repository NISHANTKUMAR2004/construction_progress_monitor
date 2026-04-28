import torch
from torch.utils.data import DataLoader
from src.dataset import ChangeDetectionDataset
from src.model import SiameseChangeDetector

def train_model():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # Dataset
    dataset = ChangeDetectionDataset("data/raw/LEVIR-CD/train")
    loader = DataLoader(dataset, batch_size=8, shuffle=True)

    # Model
    model = SiameseChangeDetector().to(device)

    # Loss
    criterion = torch.nn.BCEWithLogitsLoss(
        pos_weight=torch.tensor([3.0]).to(device)
    )

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)

    # Scheduler
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=10, gamma=0.5
    )

    # Training loop
    for epoch in range(35):
        total_loss = 0

        for img1, img2, label in loader:

            # 🔥 GPU usage (IMPORTANT)
            img1 = img1.to(device)
            img2 = img2.to(device)
            label = label.to(device)

            output = model(img1, img2)

            output = torch.nn.functional.interpolate(
                output, size=(256, 256), mode='bilinear'
            )

            loss = criterion(output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        scheduler.step()

        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, LR: {optimizer.param_groups[0]['lr']}")

    torch.save(model.state_dict(), "model.pth")
    print("Model saved!")