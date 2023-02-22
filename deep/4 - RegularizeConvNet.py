import torch
from torch import nn
from torch.utils.data import DataLoader
import numpy as np
from torchvision import transforms as T

def get_normalize(features: torch.Tensor):
    means = features.mean(axis=(0, 2, 3))
    stds = features.std(axis=(0, 2, 3))
    return means, stds

def get_augmentations(train: bool = True) -> T.Compose:
    means = np.array([0.49139968, 0.48215841, 0.44653091])
    std = np.array([0.24703223, 0.24348513, 0.26158784])
    if train:
        return T.Compose(
            [
                T.Resize(size=(224, 224)),
                T.RandAugment(),
                T.ToTensor(),
                T.Normalize(mean=means, std=std)
            ]
        )
    else:
        return T.Compose(
            [
                T.Resize(size=(224, 224)),
                T.ToTensor(),
                T.Normalize(mean=means, std=std)
            ]
        )


@torch.inference_mode()
def predict(model: nn.Module, loader: DataLoader, device: torch.device):
    model.to(device)
    model.eval()
    predictions = []
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        output = model(x)
        predictions.append(torch.argmax(output, axis=1))
    return torch.concat(predictions)


def create_simple_conv_cifar():
    return nn.Sequential(
        nn.Conv2d(in_channels=3, out_channels=16,
                  kernel_size=3, padding=1),  # 32 x 32 x 16
        nn.ReLU(),

        nn.MaxPool2d(2),  # 16 x 16 x 16

        nn.Conv2d(in_channels=16, out_channels=32,
                  kernel_size=3, padding=1),  # 16 x 16 x 32
        nn.ReLU(),

        nn.MaxPool2d(2),  # 8 x 8 x 32

        nn.Flatten(),

        nn.Linear(8 * 8 * 32, 1024),
        nn.ReLU(),
        nn.Linear(1024, 128),
        nn.ReLU(),
        nn.Linear(128, 10)
    )


@torch.inference_mode()
def predict_tta(model: nn.Module, loader: DataLoader, device: torch.device, iterations: int = 2):
    model.to(device)
    model.eval()
    iter_list = []
    outputs_list = []
    for i in range(iterations):
        for x, _ in loader:
            x = x.to(device)
            output = model(x)
            outputs_list.append(output)
        iter_list.append(torch.concat(outputs_list))
        outputs_list = []
    big_tensor = torch.stack(iter_list, dim=2)
    big_tensor = torch.mean(big_tensor, dim=2)
    return torch.argmax(big_tensor, axis=1)
