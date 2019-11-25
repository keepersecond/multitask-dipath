from torch.utils import model_zoo
from torchvision.models.resnet import ResNet, model_urls as resnet_urls, BasicBlock, Bottleneck
from mtdipath.components import FeaturesInterface


class NoHeadResNet(ResNet, FeaturesInterface):
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return self.layer4(x)


def build_resnet(pretrained=False, arch="resnet50", model_class=NoHeadResNet, **kwargs):
    """Constructs a ResNet-18 model.

    Args:
        arch (str): Type of densenet (among: resnet18, resnet34, resnet50, resnet101 and resnet152)
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        model_class (nn.Module): Actual resnet module class
    """
    params = {
        "resnet18": [BasicBlock, [2, 2, 2, 2]],
        "resnet34": [BasicBlock, [3, 4, 6, 3]],
        "resnet50": [Bottleneck, [3, 4, 6, 3]],
        "resnet101": [Bottleneck, [3, 4, 23, 3]],
        "resnet152":  [Bottleneck, [3, 8, 36, 3]]
    }
    model = model_class(*params[arch], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(resnet_urls[arch]))
    return model