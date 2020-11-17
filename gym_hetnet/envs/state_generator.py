import numpy as np
from os.path import exists
from time import sleep
import logging
import pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s: %(message)s')

class StateGenerator():

  def __init__(self, maxMacro, maxFento1, maxFento2, fileName="hetnetState_serialized",debug=False):

    # Logging stuff
    self.logger = logging.getLogger(__name__)
    if(debug):
      self.logger.setLevel(logging.DEBUG)
    else:
      self.logger.setLevel(logging.INFO)
    self.maxMacro = maxMacro
    self.maxFento1 = maxFento1
    self.maxFento2 = maxFento2
    self.S1, self.S2,self.S3,self.S4M,self.S5M = (maxMacro,maxMacro,maxMacro,maxMacro,maxMacro)
    self.S4F1 = maxFento1
    self.S5F2 = maxFento2
    self.E = 18
    self.file_name = fileName
    self.events = {
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

    if not self.loadGeneratedStates():
      self.logger.warning(f"The state file {fileName}.pkl was not found. Generating states...")
      sleep(5)
      self.logger.info("State Generator in progress...")
      self.generateStates()
      self.logger.info("State Generator done")
      
    if not self.loadGeneratedIndices():
      self.logger.warning(f"The index file {fileName}-inverse.pkl was not found. Generating indices...")
      sleep(5)
      self.logger.info("Index Generator in progress...")
      self.generateIndices()
      self.logger.info("Index Generator done")

  def stateIsPossible(self,s1,s2,s3,s4m,s5m,s4f1,s5f2,e):
    eventType, cellType, comment = self.events[e]
    sessionsMacro = s1+s2+s3+s4m+s5m
    
    # Exceeds Max Capacity
    if (sessionsMacro > self.maxMacro): return False
    if (s4f1 > self.maxFento1): return False
    if (s5f2 > self.maxFento2): return False
    
    # To Leave from Empty
    sessionsSubArea = [s1,s2,s3,s4m,s5m]

    if (eventType == "leave") and (cellType == "macro") \
      and (sessionsSubArea[comment-1] <= 0): return False
    if (eventType == "leave") and (cellType == "fento1") \
      and (s4f1 == 0): return False
    if (eventType == "leave") and (cellType == "fento2") \
      and (s5f2 == 0 ): return False

    # Impossible Handoffs from Empty
    if (eventType == "handoff"):
      if (comment == "in"):
        if (s3 <= 0): return False
      elif (cellType == "fento1") and (s4f1 <= 0): return False
      elif (cellType == "fento2") and (s5f2 <= 0): return False
    
    return True

  def generateStates(self):
    S1,S2,S3,S4M,S5M = self.S1, self.S2, self.S3, self.S4M, self.S5M
    S4F1,S5F2, E = self.S4F1, self.S5F2, self.E

    states = []
    for s1 in range(S1+1):
      self.logger.debug(f"S1={s1+1}/{S1+1}")
      for s2 in range(S2+1):
        if (s1 + s2) > self.maxMacro: break
        for s3 in range(S3+1):
          if (s1 + s2 + s3) > self.maxMacro: break
          for s4m in range(S4M+1):
            if (s1 + s2 + s3 + s4m) > self.maxMacro: break
            for s5m in range(S5M+1):
              if (s1 + s2 + s3 + s4m + s5m) > self.maxMacro: break
              for s4f1 in range(S4F1+1):
                for s5f2 in range(S5F2+1):
                  for e in range(1,E+1):
                    if not self.stateIsPossible(s1,s2,s3,s4m,s5m,s4f1,s5f2,e):
                      continue
                    state = [s1,s2,s3,s4m,s5m,s4f1,s5f2,e]
                    states.append(state)
    states = np.array(states)
    self.states = states
    self.saveGeneratedStates()

  def generateIndices(self):
    states = self.states
    indices = {}
    for i in range(len(states)):
      state = states[i]
      state = str(state)
      indices.update({state:i})
    self.indices = indices
    self.saveGeneratedIndices()

  def saveGeneratedStates(self):
    with open(self.file_name + ".pkl", "wb") as file:
      np.save(file, self.states)

  def loadGeneratedStates(self):
    if exists(self.file_name + '.pkl'):
        self.logger.debug(f"State file {self.file_name}.pkl found")
        self.states = np.load(self.file_name + ".pkl")
        return True
    return False

  def saveGeneratedIndices(self):
    file_name = self.file_name + "-inverse.pkl"
    with open(file_name,"wb") as file:
      pickle.dump(self.indices, file)
      
  def loadGeneratedIndices(self):
    file_name = self.file_name + "-inverse.pkl"
    if exists(file_name):
      self.logger.debug(f"State file {file_name} found")
      with open(file_name,"rb") as file:
        indices = pickle.load(file)
        self.indices = indices
      return True
    return False