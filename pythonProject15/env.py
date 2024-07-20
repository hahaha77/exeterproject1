import gym
from gym import spaces
import numpy as np

class BreastCancerEnv(gym.Env):
    def __init__(self, state_data, action_data):
        super(BreastCancerEnv, self).__init__()
        self.state_data = state_data
        self.action_data = action_data
        self.observation_space = spaces.Box(low=-1, high=1, shape=(state_data.shape[1],), dtype=np.float32)
        self.action_space = spaces.Discrete(8)  # Actions: chemotherapy, hormone therapy, radio therapy
        self.state = None
        self.current_index = None
        self.current_step = 0

    def reset(self):
        self.current_step = 0
        self.current_index = np.random.choice(self.state_data.shape[0])
        self.state = self.state_data.iloc[self.current_index].values
        return self.state

    def step(self, action):
        # print(action)
        # action_decoded = np.array(list(np.binary_repr(action, width=3)), dtype=int)
        actual_action = self.action_data.iloc[self.current_index].values
        fb = np.random.uniform(0, 1)
        reward = self.calculate_reward(action, actual_action, fb)
        done = self.current_step >= len(self.state_data)
        self.current_step += 1

        # Move to the next state
        if not done:
            self.current_index = (self.current_index + 1) % self.state_data.shape[0]
            self.state = self.state_data.iloc[self.current_index]
        else:
            self.state = None

        return self.state, reward, done, {}

    def calculate_reward(self, action, actual_action, user_feedback=0.0):
        reward = 0
        # print(action, actual_action)
        v = np.abs(action - actual_action)
        if np.sum(v) == 0:
            reward += 10
        elif np.sum(v) == 1:
            reward += 3
        elif np.sum(v) > 2:
            reward -= 15
        else:
            treatment_effectiveness = 2 - np.sum(v) / len(action)
            reward += treatment_effectiveness + user_feedback*5
        return reward


