import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import logging
from pathlib import Path
import json
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalImageDataset(Dataset):
    """Dataset class for medical images"""

    def __init__(self, image_paths: List[str], labels: List[int], transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image (simplified - in production, handle DICOM, etc.)
        image = torch.randn(3, 224, 224)  # Mock image tensor
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label


class MedicalImageClassifier(nn.Module):
    """CNN for medical image classification"""

    def __init__(self, num_classes: int = 4):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((7, 7))
        )

        self.classifier = nn.Sequential(
            nn.Linear(256 * 7 * 7, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


class MedicalModelTrainer:
    """Trainer for medical AI models"""

    def __init__(self, model_save_path: str = "models"):
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

    def train_image_classifier(self, train_data: Dict[str, List],
                               val_data: Dict[str, List],
                               num_epochs: int = 10) -> Dict[str, Any]:
        """Train medical image classifier"""

        # Create datasets
        train_dataset = MedicalImageDataset(
            train_data["image_paths"],
            train_data["labels"]
        )
        val_dataset = MedicalImageDataset(
            val_data["image_paths"],
            val_data["labels"]
        )

        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

        # Initialize model
        model = MedicalImageClassifier(num_classes=4)
        model.to(self.device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

        # Training loop
        train_losses = []
        val_accuracies = []

        for epoch in range(num_epochs):
            model.train()
            epoch_loss = 0.0

            for batch_idx, (data, targets) in enumerate(train_loader):
                data, targets = data.to(self.device), targets.to(self.device)

                optimizer.zero_grad()
                outputs = model(data)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()

            # Validation
            val_acc = self._evaluate_model(model, val_loader)

            avg_loss = epoch_loss / len(train_loader)
            train_losses.append(avg_loss)
            val_accuracies.append(val_acc)

            logger.info(f"Epoch [{epoch + 1}/{num_epochs}] - "
                        f"Loss: {avg_loss:.4f}, Val Acc: {val_acc:.4f}")

            scheduler.step()

        # Save model
        model_path = self.model_save_path / "medical_image_classifier.pth"
        torch.save({
            'model_state_dict': model.state_dict(),
            'model_config': {
                'num_classes': 4,
                'architecture': 'custom_cnn'
            },
            'training_history': {
                'train_losses': train_losses,
                'val_accuracies': val_accuracies
            }
        }, model_path)

        logger.info(f"Model saved to {model_path}")

        # Generate training report
        self._generate_training_report(train_losses, val_accuracies, "image_classifier")

        return {
            'final_val_accuracy': val_accuracies[-1],
            'training_history': {
                'train_losses': train_losses,
                'val_accuracies': val_accuracies
            },
            'model_path': str(model_path)
        }

    def _evaluate_model(self, model, data_loader) -> float:
        """Evaluate model performance"""
        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for data, targets in data_loader:
                data, targets = data.to(self.device), targets.to(self.device)
                outputs = model(data)
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()

        return correct / total

    def _generate_training_report(self, train_losses: List[float],
                                  val_accuracies: List[float],
                                  model_name: str):
        """Generate training report with visualizations"""

        # Create results directory
        results_dir = Path("results/experiments")
        results_dir.mkdir(parents=True, exist_ok=True)

        # Plot training curves
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Training loss
        ax1.plot(train_losses)
        ax1.set_title('Training Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.grid(True)

        # Validation accuracy
        ax2.plot(val_accuracies)
        ax2.set_title('Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.grid(True)

        plt.tight_layout()
        plt.savefig(results_dir / f"{model_name}_training_curves.png", dpi=300, bbox_inches='tight')
        plt.close()

        # Save metrics to JSON
        metrics = {
            'model_name': model_name,
            'final_train_loss': train_losses[-1],
            'final_val_accuracy': val_accuracies[-1],
            'best_val_accuracy': max(val_accuracies),
            'training_epochs': len(train_losses),
            'metrics_history': {
                'train_losses': train_losses,
                'val_accuracies': val_accuracies
            }
        }

        with open(results_dir / f"{model_name}_metrics.json", 'w') as f:
            json.dump(metrics, f, indent=2)

        logger.info(f"Training report saved to {results_dir}")


def main():
    """Main training function"""
    trainer = MedicalModelTrainer()

    # Mock training data (in production, load real data)
    train_data = {
        "image_paths": [f"data/train/image_{i}.jpg" for i in range(800)],
        "labels": [i % 4 for i in range(800)]  # 4 classes: X-ray, MRI, CT, Ultrasound
    }

    val_data = {
        "image_paths": [f"data/val/image_{i}.jpg" for i in range(200)],
        "labels": [i % 4 for i in range(200)]
    }

    # Train model
    results = trainer.train_image_classifier(train_data, val_data, num_epochs=20)

    logger.info("Training completed successfully!")
    logger.info(f"Final validation accuracy: {results['final_val_accuracy']:.4f}")


if __name__ == "__main__":
    main()