import gymnasium as gym
from env import PingPongGame
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
import imageio
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import pygame

from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

class RewardLoggerCallback(BaseCallback):
    def __init__(self):
        super(RewardLoggerCallback, self).__init__()
        self.rewards = []

    def _on_step(self) -> bool:
        # Record the reward of the current step
        self.rewards.append(self.locals["rewards"])
        return True

env = PingPongGame()

# sarqi dql model
model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0001)
timesteps = 1000
reward_callback = RewardLoggerCallback()

model.learn(timesteps, callback = reward_callback)

# testing ev amen tesarani pahum
env = PingPongGame()
obs, _ = env.reset()

frames = []

for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, _, done, _, _ = env.step(action)

    screen = env.render("training")
    frame = pygame.surfarray.array3d(screen)
    frame = frame.swapaxes(0, 1)

    frames.append(frame)
    if done:
        break

# pahir inchpes gif
gif_path = "ping_pong_game.gif"
imageio.mimsave(gif_path, frames, duration=1/30)


import matplotlib.pyplot as plt
rewards = np.array(reward_callback.rewards)
aggregated_rewards = rewards.reshape(-1, 100).mean(axis=1)
plt.plot(aggregated_rewards)
plt.show()