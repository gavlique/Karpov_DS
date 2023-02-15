import torch

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
    