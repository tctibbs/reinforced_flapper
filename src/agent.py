"""DQN agent training script for Flappy Bird."""

from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env

from src.flappy_env import FlappyBirdEnv

# Create the environment
env = make_vec_env(FlappyBirdEnv, n_envs=1)

# Initialize the DQN model
model = DQN(
    "CnnPolicy",
    env,
    verbose=1,
    buffer_size=10000,
    learning_starts=1000,
    batch_size=32,
    target_update_interval=500,
)

# Train the model
model.learn(total_timesteps=100000)

# Save the model
model.save("dqn_flappybird")

# Load the model
model = DQN.load("dqn_flappybird")

# Test the trained model
obs = env.reset()
for _i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
