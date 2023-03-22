import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as f
from torch import optim
from torch import save
import torch

class ChessValueDataset(Dataset):
    def __init__(self):
        data = np.load("data/dataset_6000.npz", allow_pickle=True)
        self.X = data["arr_0"]
        self.Y = data["arr_1"]
        print("loaded", self.X.shape, self.Y.shape)

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.a1 = nn.Conv2d(5, 16, kernel_size=3, padding=1)
        self.a2 = nn.Conv2d(16, 16, kernel_size=3, padding=1)
        self.a3 = nn.Conv2d(16, 32, kernel_size=3, stride=2)

        self.b1 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.b3 = nn.Conv2d(32, 64, kernel_size=3, stride=2)
    
        self.c1 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c2 = nn.Conv2d(64, 64, kernel_size=2, padding=1)
        self.c3 = nn.Conv2d(64, 128, kernel_size=2, stride=2)

        self.d1 = nn.Conv2d(128, 128, kernel_size=1)
        self.d2 = nn.Conv2d(128, 128, kernel_size=1)
        self.d3 = nn.Conv2d(128, 128, kernel_size=1)

        self.last = nn.Linear(128, 1)

    def forward(self, x):
        x = f.relu(self.a1(x))
        x = f.relu(self.a2(x))
        x = f.relu(self.a3(x))

        # 4x4
        x = f.relu(self.b1(x))
        x = f.relu(self.b2(x))
        x = f.relu(self.b3(x))

        # 2x2
        x = f.relu(self.c1(x))
        x = f.relu(self.c2(x))
        x = f.relu(self.c3(x))

        # 1x128
        x = f.relu(self.d1(x))
        x = f.relu(self.d2(x))
        x = f.relu(self.d3(x))

        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return f.tanh(x)


if __name__ == '__main__':
    dataset = ChessValueDataset()
    device = torch.device("mps")
    train_loader = DataLoader(dataset, batch_size=256, shuffle=True)
    model = NeuralNetwork()
    optimizer = optim.Adam(model.parameters())
    floss = nn.MSELoss()
    model = model.to(device)
    
    for epoch in range(100):
        all_loss = 0
        num_loss = 0
        for idx, (input, labels) in enumerate(train_loader):
            print(idx)
            # print(f"Feature batch shape: {input.size()}")
            # print(f"Labels batch shape: {labels.size()}")
            labels = labels.unsqueeze(-1)

            input, labels = input.to(torch.device("mps")), labels.to(torch.device("mps"))
            input = input.float()
            labels = labels.float()

            # zero the gradient buffers
            optimizer.zero_grad()

            # Forward Propagation: In forward prop, the NN makes its best guess about the correct output.
            # It runs the input data through each of its functions to make this guess.
            output = model(input)  # forward pass
            
            loss = floss(output, labels)

            # Backward Propagation: In backprop, the NN adjusts its parameters proportionate to the error in its guess.
            # It does this by traversing backwards from the output,
            # collecting the derivatives of the error with respect to the parameters of the functions (gradients),
            # and optimizing the parameters using gradient descent
            loss.backward()

            # update weights
            optimizer.step()

            all_loss += loss.item()
            num_loss += 1

        print("%3d: %f" % (epoch, all_loss / num_loss))
        save(model.state_dict(), "nets/value.pth")
