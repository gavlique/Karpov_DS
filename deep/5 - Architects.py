from torch import nn
from torchvision.models import alexnet, vgg11, googlenet, resnet18

def get_pretrained_model(model_name: str, num_classes: int, pretrained: bool=True):
    model = None
    if model_name == 'alexnet':
        model = alexnet(pretrained=pretrained)
        model.classifier[6] = nn.Linear(
            in_features=4096, out_features=num_classes)
    elif model_name == 'vgg11':
        model = vgg11(pretrained=pretrained)
        model.classifier[6] = nn.Linear(
            in_features=4096, out_features=num_classes)
    elif model_name == 'googlenet':
        model = googlenet(pretrained=pretrained)
        model.fc = nn.Linear(
            in_features=1024, out_features=num_classes)
        model.aux1.fc2 = nn.Linear(
            in_features=1024, out_features=num_classes)
        model.aux2.fc2 = nn.Linear(
            in_features=1024, out_features=num_classes)
    elif model_name == 'resnet18':
        model = resnet18(pretrained=pretrained)
        model.fc = nn.Linear(
            in_features=512, out_features=num_classes)
    return modeladdd


# class ResNet9(nn.Module):
#     def _make_conv_block(self, in_features, out_features):
#         return nn.Sequential(
#             nn.Conv2d(in_features, out_features,
#                         kernel_size=3, padding=1, bias=True),
#             nn.BatchNorm2d(out_features),
#             nn.ReLU()
#         )

#     def _make_pooling(self, size=2):
#         return nn.MaxPool2d(kernel_size=size, stride=size)

#     def __init__(self):
#         super().__init__()  # 32x32x3
#         self.conv_1 = self._make_conv_block(3, 64)  # 32x32x64
#         self.conv_2 = nn.Sequential(
#             self._make_conv_block(64, 128),
#             self._make_pooling()
#         )  # 16x16x128
#         self.res_1 = nn.Sequential(
#             self._make_conv_block(128, 128),
#             self._make_conv_block(128, 128)
#         )  # 16x16x128
#         self.conv_3 = nn.Sequential(
#             self._make_conv_block(128, 256),
#             self._make_pooling()
#         )  # 8x8x256
#         self.conv_4 = nn.Sequential(
#             self._make_conv_block(256, 512),
#             self._make_pooling()
#         )  # 4x4x512
#         self.res_2 = nn.Sequential(
#             self._make_conv_block(512, 512),
#             self._make_conv_block(512, 512)
#         )  # 4x4x512
#         self.clas = nn.Sequential(
#             self._make_pooling(4),  # 1x1x512
#             nn.Flatten(),
#             nn.Linear(512, 10)
#         )

#     def forward(self, x):
#         out = self.conv_1(x)
#         out = self.conv_2(out)
#         out = self.res_1(out) + out
#         out = self.conv_3(out)
#         out = self.conv_4(out)
#         out = self.res_2(out) + out
#         out = self.clas(out)
#         return out
           
# def create_advanced_skip_connection_conv_cifar():
#     return ResNet9()
        
