import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer

def create_model():
    return nn.Sequential(
        nn.Linear(in_features = 100, out_features = 10),
        nn.ReLU(),
        nn.Linear(in_features = 10, out_features = 1)
    )

def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
    model.train()
    total_loss = 0
    for x, y in data_loader:
        optimizer.zero_grad()  # zeroing gradients
        output = model(x)  # forward pass
        loss = loss_fn(output, y)  # count loss
        total_loss += loss.item()  # writing current loss
        loss.backward()  # backward pass
        print(round(loss.item(), 5))  # print current loss
        optimizer.step()  # optimization step
    return total_loss / len(data_loader)


def evaluate(model: nn.Module, data_loader: DataLoader, loss_fn):
    model.eval()
    with torch.no_grad(): # we need to turn off gradients for evaluation
        total_loss = 0
        for x, y in data_loader:
            output = model(x)
            loss = loss_fn(output, y)
            total_loss += loss.item()
    return total_loss / len(data_loader)
