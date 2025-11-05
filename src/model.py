"""This module defines the Deep Q-Network (DQN) model using PyTorch."""

import torch
import torch.nn as nn


class DQN(nn.Module):
    """Deep Q-Network (DQN) model.

    Attributes:
        input_shape: The shape of the input state.
        num_actions: The number of possible actions.
        features: Convolutional layers to extract features from the input state.
        fc: Fully connected layers to produce Q-values for each action.
    """

    def __init__(self, input_shape: tuple[int, int, int], num_actions: int) -> None:
        """Initializes the DQN model.

        Args:
            input_shape: The shape of the input state.
            num_actions: The number of possible actions.
        """
        super().__init__()
        self.input_shape = input_shape
        self.num_actions = num_actions

        self.features = nn.Sequential(
            nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Linear(self.feature_size(), 512), nn.ReLU(), nn.Linear(512, num_actions)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass of the DQN model.

        Args:
            x: The input tensor representing the state.

        Returns:
            The Q-values for each action.
        """
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

    def feature_size(self) -> int:
        """Computes the size of the output of the convolutional layers.

        Returns:
            The size of the flattened output from the convolutional layers.
        """
        return self.features(torch.zeros(1, *self.input_shape)).view(1, -1).size(1)
