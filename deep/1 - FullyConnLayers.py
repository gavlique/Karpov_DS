import torch
from torch import nn

def function01(tensor: torch.Tensor, count_over: str) -> torch.Tensor:
    if count_over == 'columns':
        result = tensor.mean(dim=0)
    if count_over == 'rows':
        result = tensor.mean(dim=1)
    return result

def function02(tensor: torch.Tensor) -> torch.Tensor:
    w = torch.rand(tensor.shape[1], requires_grad=True, dtype=torch.float32)
    return w

def function03(x: torch.Tensor, y: torch.Tensor):
    step=1e-2
    mse = 2
    w = function02(x)
    while (mse > 1):
        y_pred = x @ w
        mse = torch.mean((y - y_pred) ** 2)
        print(mse)

        mse.backward()

        with torch.no_grad():
            w += -w.grad * step
            
        w.grad.zero_()
    return w

def function04(x: torch.Tensor, y: torch.Tensor):
    step=1e-2
    mse = 2
    layer = nn.Linear(in_features = x.shape[1], out_features = 1)
    while (mse > 0.3):
        y_pred = layer(x).ravel()
        mse = torch.mean((y - y_pred) ** 2)
        print(mse)

        mse.backward()

        with torch.no_grad():
            layer.weight += -layer.weight.grad * step
            layer.bias += -layer.bias.grad * step
            
        layer.zero_grad()
    return layer
            