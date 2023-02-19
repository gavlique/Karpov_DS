from torch import nn

def count_parameters_conv(in_channels: int, out_channels: int, kernel_size: int, bias: bool):
    return (in_channels * kernel_size ** 2 + bias) * out_channels


def create_mlp_model():
    return nn.Sequential(
        nn.Flatten(),
        nn.Linear(in_features=28*28, out_features=256),
        nn.ReLU(),
        nn.Linear(in_features=256, out_features=10)
    )


def create_conv_model():
    return nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        nn.Flatten(),
        nn.Linear(4 * 4 * 64, 256),
        nn.ReLU(),
        nn.Linear(256, 10)
    )