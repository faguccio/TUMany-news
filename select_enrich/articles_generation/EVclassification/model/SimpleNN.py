import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Define a simple 2-layer neural network
class SimpleNN(nn.Module):
    def __init__(self, input_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)  # First layer with 64 neurons
        self.relu = nn.ReLU()               # Activation function
        self.fc2 = nn.Linear(16, 8)         # Output layer
        self.relu = nn.ReLU() 
        self.fc3 = nn.Linear(8, 4)  # First layer with 64 neurons
        self.relu = nn.ReLU()               # Activation function
        self.fc4 = nn.Linear(4, 1)         # Output layer
        self.sigmoid = nn.Sigmoid()         # Sigmoid for binary classification

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        
        x = self.sigmoid(x)
        return x