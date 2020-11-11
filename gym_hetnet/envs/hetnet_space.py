import numpy as np
from gym.spaces import Discrete

class HetnetSpace(Discrete):

    def __init__(self, n):
        self.map_index_state = np.array([[0,0,0],[1,0,1]]) # ya estan definidos
        self.map_states_index = {"[0, 0, 0]": 0, "[1, 0, 1]":1}
        super(HetnetSpace, self).__init__(n)

    def sample(self):
        rand_index = self.np_random.randint(self.n)
        return self.map_index_state[rand_index]

    def contains(self,x):
        if isinstance(x,int):
            return ( x <= len(self.map_index_index) )
        elif isinstance(x, list):
            return self.map_states_index.get(str(x),None) is not None
        elif isinstance(x,np.ndarray):
            return self.map_states_index.get(str(list(x)), None) is not None 
        else:
            raise Exception(f"Operator {x} does not match with type")
    
            