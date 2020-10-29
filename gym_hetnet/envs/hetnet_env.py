import gym
from gym import error, spaces, utils
from gym.utils import seeding

class HetnetEnv(gym.Env):
  metadata = {'render.modes': ['human']}
  Qtable = None

  def __init__(self):
    nActions = 3
    nStates = 10
    self.action_space = spaces.Discrete(nActions)
    self.observation_space = spaces.Discrete(nStates)

  def step(self, action):
    observation = 0  # TODO
    reward = 0       # TODO
    done = True      # Supongo que nunca llega a Done o solo con 0 users
    info = {}
    return observation, reward, done, info

  def reset(self):
    observation = self.observation_space.sample()
    return observation

  def render(self, mode='human'):
    raise NotImplementedError

  def close(self):
    raise NotImplementedError