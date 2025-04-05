import torch
import torch.nn as nn
import torch.nn.functional as F

BOARD_SIZE = 15


class ValueNetwork(nn.Module):
    def __init__(self, in_channels=2):
        super(ValueNetwork, self).__init__()
        # Convolutional layers to extract spatial features
        self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=3, padding=1)  # Output: 32 x 15 x 15
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # Output: 64 x 15 x 15
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)  # Output: 64 x 15 x 15

        # Fully connected layers to output a single value
        self.fc1 = nn.Linear(64 * BOARD_SIZE * BOARD_SIZE, 256)
        self.fc2 = nn.Linear(256, 1)

    def forward(self, x):
        """
        x: Tensor of shape (batch_size, in_channels, BOARD_SIZE, BOARD_SIZE)
        """
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        # Tanh squashes the output to (-1, 1), representing the value of the state.
        x = torch.tanh(self.fc2(x))
        return x


if __name__ == '__main__':
    net = ValueNetwork()
    # 예: 배치 사이즈 1, 2 채널, 15x15 보드
    dummy_input = torch.randn(1, 2, BOARD_SIZE, BOARD_SIZE)
    output = net(dummy_input)
    print("Value network output:", output)
