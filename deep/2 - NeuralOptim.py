import torch
from torch import nn

def create_model():
    return nn.Sequential(
        nn.Linear(in_features = 100, out_features = 10),
        nn.ReLU(),
        nn.Linear(in_features = 10, out_features = 1)
    )

def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
    