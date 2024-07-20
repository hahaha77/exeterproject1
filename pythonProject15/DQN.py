import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return torch.softmax(x, dim=-1)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQN(state_size, action_size).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return [random.randrange(2) for _ in range(self.action_size)]
        state = np.array(state, dtype=float)
        state = torch.FloatTensor(state).unsqueeze(0).to(device)
        act_values = self.model(state).squeeze()
        # print(np.argmax(act_values), act_values)

        return (act_values.cpu().detach().numpy() >= 0.5).astype(int)
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = np.array(state, dtype=float)
            next_state = np.array(next_state, dtype=float)

            state = torch.FloatTensor(state).to(device)
            next_state = torch.FloatTensor(next_state).to(device)
            reward = torch.tensor(reward).float().to(device)
            target = reward if done else reward + self.gamma * torch.max(self.model(next_state)).item()
            target_f = self.model(state).clone().detach()
            target_f[action] = target.type(target_f.dtype)
            self.optimizer.zero_grad()
            loss = self.criterion(target_f, self.model(state))
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_state_dict(torch.load(name))

    def save(self, name):
        torch.save(self.model.state_dict(), name)


