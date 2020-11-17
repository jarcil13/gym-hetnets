import gym
from gym import error, utils
from gym.utils import seeding
from gym import spaces
from hetnet_space import HetnetSpace

map_state = {
  'S1'  : 0,
  'S2'  : 1,
  'S3'  : 2,
  'S4M' : 3,
  'S4f1': 4,
  'S5M' : 5,
  'S5f2': 6,
}

Events = {
    1:  ("enter","macro",1),
    2:  ("enter","macro",2),
    3:  ("enter","macro",3),
    4:  ("enter","macro",4),
    5:  ("enter","fento1",""),
    6:  ("enter","macro",5),
    7:  ("enter","fento2",""),
    8:  ("handoff","fento1","out"),
    9:  ("handoff","fento1","in"),
    10: ("handoff","fento2","out"),
    11: ("handoff","fento2","in"),
    12: ("leave","macro",1),
    13: ("leave","macro",2),
    14: ("leave","macro",3),
    15: ("leave","macro",4),
    16: ("leave","fento1",""),
    17: ("leave","macro",5),
    18: ("leave","fento2","")
}

code_event_macro_in = [0,1,2,3,5,7,9]
code_event_macro_out = [8,10,11,12,13,14,16]

class HetnetEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, MacroMaxCapacity=2, FentoMaxCapacity=1):
    self.MacroMaxCapacity = MacroMaxCapacity
    self.FentoMaxCapacity = FentoMaxCapacity
    self.observation_space = HetnetSpace((2,2,2))
    self.action_space = spaces.Discrete(3)
    self.reset()
  
  def __setVariables(self,vars,):
    self.s1   = vars[0]
    self.s2   = vars[1]
    self.s3   = vars[2]
    self.s4m  = vars[3]
    self.s5m  = vars[4]
    self.s4f1 = vars[5]
    self.s5f2 = vars[6]
    self.e    = vars[7]
 
  def stateToIndex(self):
    vars = str([self.s1,self.s2,self.s3,self.s4m,self.s5m,self.s4f1,self.s5f2,self.e])
    self.observation_space.map_state_index(vars)

  def __Macro_connections(self):
    state = self.observation_space.nvec
    return state[map_state['S1']] + state[map_state['S2']] + state[map_state['S3']] + state[map_state['S4M']] + state[map_state['S5M']]
  
  # Action 0-accept 1-reject 2-continue
  def step(self, action):
    assert self.action_space.contains(action)
    reward = 0
    if action == 0:
      return self., reward, False, {}
    elif action == 1:
      new_e = randEvent()
      self.e = new_e
      return self.stateToIndex(), reward, done(falta), {}
    elif action == 2:
    else:
      raise Exception(f"Action: {action} not defined")

    
    # reward = 0
    # if action == 2: # If action is continue, do nothing and continue
    #   return self.observation_space.nvec, reward, False, {}

    # actual_event = self.action_space.nvec[-1]
    
    # elif action == 0: # If action in accept
    #   Events[actual_event] == Lo que tiene que ver con macro 
    
    # elif action == 1:

    # # This statement should be unreacheable.
    # else:  # But, just in case :D
    #   raise Exception(f"Action: {action} not defined")



    # elif action == 0: 
    #   if self.__Macro_connections() < self.MacroMaxCapacity: # Can accept
    #     self.__accept_connection_Macro()
    #   else: # Can't accept connection to macro. State impossible
    #     reward = -1

    # elif action == 1:
    #   if self.observation_space.nvec[map_state['S4f1']] < self.FentoMaxCapacity # Can accept
    #     self.observation_space.nvec[map_state['S4f1']] += 1
    #   else:  # Can't accept connection to Fento 1 (S4). State impossible
    #     reward = -1
    # elif action == 2:
    #   if self.observation_space.nvec[map_state['S5f2']] < self.FentoMaxCapacity # Can accept
    #     self.observation_space.nvec[map_state['S5f2']] += 1
    #   else:  # Can't accept connection to Fento 2 (S5). State impossible
    #     reward = -1

    # elif action == 3:
    #   if self.__Macro_connections() > 0: # Can release connection
    #     self.__release_connection_Macro()
    #   else: # Can't release connection if Macro is empty. State impossible
    #     reward = -1

    # elif action == 4:
    #   if self.observation_space.nvec[map_state['S4f1']] > 0: # Can release connection
    #     self.observation_space.nvec[map_state['S4f1']] -= 1
    #   else:  # Can't release connection if Fento 1 (S4) is empty. State impossible
    #     reward = -1

    # elif action == 5:
    #   if self.observation_space.nvec[map_state['S5f2']] > 0: # Can release connection
    #     self.observation_space.nvec[map_state['S5f2']] -= 1
    #   else:  # Can't release connection if Fento 2 (S5) is empty. State impossible
    #     reward = -1

    # elif action == 6:
    #    # Check if can handoff a connection form Macro to S4f1
    #    if self.__Macro_connections() > 0 and self.observation_space.nvec[map_state['S4f1']] < self.FentoMaxCapacity
    #       reward = 10
    #       self.__release_connection_Macro()
    #       self.observation_space.nvec[map_state['S4f1']] += 1
    #    else: # Impossible to do handoff
    #      reward = -1

    # elif action == 7:
    #   # Check if can handoff a connection form Macro to S5f2
    #    if self.__Macro_connections() > 0 and self.observation_space.nvec[map_state['S5f2']] < self.FentoMaxCapacity
    #       reward = 10
    #       self.__release_connection_Macro()
    #       self.observation_space.nvec[map_state['S5f2']] += 1
    #    else: # Impossible to do handoff
    #      reward = -1

    # elif action == 8:
    #   # Check if can hadoff a connection from S4f1 to Macro
    #   if self.observation_space.nvec[map_state['S4f1']] > 0 and self.__Macro_connections() < self.MacroMaxCapacity:
    #     reward = 10
    #     self.__accept_connection_Macro()
    #     self.observation_space.nvec[map_state['S4f1']] -= 1
    #   else: #  Impossible to do handoff
    #     reward = -1

    # elif action == 9:
    #   # Check if can hadoff a connection from S4f1 to Macro
    #   if self.observation_space.nvec[map_state['S5f2']] > 0 and self.__Macro_connections() < self.MacroMaxCapacity:
    #     reward = 10
    #     self.__accept_connection_Macro()
    #     self.observation_space.nvec[map_state['S5f2']] -= 1
    #   else: #  Impossible to do handoff
    #     reward = -1
    
    
    
    # Finally, we used the observation space with the changes made by the action
    observation = self.observation_space.nvec
    done = False # Stop the simulation is not implemented yet :D 
    info = {}
    # And return everything
    return observation, reward, done, info

  def reset(self):
    observation_index = self.observation_space.sample()
    self.__setVariables(self.observation_space.map_index_state[observation_index])
    return observation_index

  def render(self, mode='human'):
    raise NotImplementedError

  def close(self):
    raise NotImplementedError