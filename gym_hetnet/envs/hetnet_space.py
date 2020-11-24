import numpy as np
from gym.spaces import Discrete
from gym_hetnet.envs.state_generator import StateGenerator

class HetnetSpace(Discrete):

    def __init__(self, maxCapacity=(2,2,2)):
        maxMacro, maxFento1, maxFento2 = maxCapacity
        state_generator = StateGenerator(maxMacro, maxFento1, maxFento2, debug=True)
        self.map_index_state = state_generator.states
        self.map_states_index = state_generator.indices
        super(HetnetSpace, self).__init__(len(state_generator.states))

    def sample(self):
        return self.np_random.randint(self.n)

    def contains(self,x):
        if isinstance(x,int):
            return ( x <= len(self.map_index_state) )
        elif isinstance(x, list):
            return self.map_states_index.get(str(x),None) is not None
        elif isinstance(x,np.ndarray):
            return self.map_states_index.get(str(list(x)), None) is not None 
        else:
            raise Exception(f"Operator {x} does not match with type")
    
            