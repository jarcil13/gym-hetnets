import gym
from gym import error, utils
from gym.utils import seeding
from gym import spaces
from gym_hetnet.envs.hetnet_space import HetnetSpace

map_state = {
  'S1'  : 0,
  'S2'  : 1,
  'S3'  : 2,
  'S4M' : 3,
  'S4f1': 4,
  'S5M' : 5,
  'S5f2': 6,
}

Actions = {
  0: "accept",
  1: "reject",
  2: "continue"
}

Events = {
    0:  ("enter","macro",1),
    1:  ("enter","macro",2),
    2:  ("enter","macro",3),
    3:  ("enter","macro",4),
    4:  ("enter","fento1",""),
    5:  ("enter","macro",5),
    6:  ("enter","fento2",""),
    7:  ("handoff","fento1","out"),
    8:  ("handoff","fento1","in"),
    9: ("handoff","fento2","out"),
    10: ("handoff","fento2","in"),
    11: ("leave","macro",1),
    12: ("leave","macro",2),
    13: ("leave","macro",3),
    14: ("leave","macro",4),
    15: ("leave","fento1",""),
    16: ("leave","macro",5),
    17: ("leave","fento2","")
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
  
  def __setVariables(self,vars):
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
    self.observation_space.map_states_index[vars]
  
  def getValidEvents(self):
    s1,s2,s3,s4m,s5m=self.s1, self.s2, self.s3, self.s4m, self.s5m
    s4f1,s5f2,e = self.s4f1, self.s5f2, self.e
    maxMacro, maxFento = self.MacroMaxCapacity, self.FentoMaxCapacity
    validEvents = []
    # Entrada
    usersMacro = s1+s2+s3+s4m+s5m
    if usersMacro < maxMacro:
      validEvents.append(0)
      validEvents.append(1)
      validEvents.append(2)
      validEvents.append(3)
      validEvents.append(5)
    if s4f1 < maxFento:
      validEvents.append(4)
    if s5f2 < maxFento:
      validEvents.append(6)
    # Handoff Sale de la Fento a la Macro
    if (s4f1 > 0) and (s3 < usersMacro):
      validEvents.append(7)
    if (s5f2 > 0) and (s3 < usersMacro):
      validEvents.append(9)
    # Handoff Entra a la fento
    if (s3 > 0) and (s4f1 < maxFento):
      validEvents.append(8)
    if (s3 > 0) and (s5f2 < maxFento):
      validEvents.append(10)
    # Salida
    if s1 > 0:
      validEvents.append(11)
    if s2 > 0:
      validEvents.append(12)
    if s3 > 0:
      validEvents.append(13)
    if s4m > 0:
      validEvents.append(14)
    if s4f1 > 0:
      validEvents.append(15)
    if s5m > 0:
      validEvents.append(16)
    if s5f2 > 0:
      validEvents.append(17)
    return validEvents

  def increaseUsers(self,zone,cell,amount):
    if zone == 1: self.s1 += amount
    elif zone == 2: self.s2 += amount
    elif zone == 3: self.s2 += amount
    elif zone == 4:
      if cell == "macro": self.s4m += amount
      elif cell == "fento1": self.s4f1 += amount
      else: raise Exception("Cell is invalid")
    elif zone == 5:
      if cell == "macro": self.s5m += amount
      elif cell == "fento2": self.s5f2 += amount
      else: raise Exception("Cell is invalid")
    else: raise Exception("Zone is invalid")

  def acceptEntrance(self,zone,cell):
    self.increaseUsers(zone,cell,1)

  def continueDeparture(self,zone,cell):
    self.increaseUsers(zone,cell,-1)

  def acceptHandoff(self, zone, cell):
    #assert() TODO
    aux = -1
    if cell == "out":
      aux = 1
    if zone == "fento1":
      self.s4f1 -= aux
      self.s3 += aux
    elif zone == "fento2":
      self.s5f2 += aux
      self.s3 -= aux
    else:
        raise Exception("Zone: s invalid")

  # Action 0-accept 1-reject 2-continue
  def step(self, action):
    assert self.action_space.contains(action)
    eventType, eventCell, eventZone = Events[self.e]
    reward = 0
    isFinalState = False
    info = {}

    if action == 0:
      if eventType == "enter":
        self.acceptEntrance(eventZone, eventCell)
        reward = 1
      elif eventType == "handoff":
        self.acceptHandoff(eventZone, eventCell)
      else:
        reward = -1
    
    elif action == 1:
      if eventType == "leave":
        reward = -1

    elif action == 2:
      if eventType == "leave":
        self.continueDeparture(eventZone, eventCell)
      else:
        reward = -1
    else: # Esto no debería ser alcanzable pero por si algo....
      raise Exception("Action: not defined")

    validEvents = getValidEvents()
    rand = np.random.uniform(low=0, high=len(validEvents)-1)
    self.e = validEvents[rand]
    return self.stateToIndex(), reward, isFinalState, info

  def reset(self):
    observation_index = self.observation_space.sample()
    self.__setVariables(self.observation_space.map_index_state[observation_index])
    return observation_index

  def render(self, mode='human'):
    raise NotImplementedError

  def close(self):
    raise NotImplementedError