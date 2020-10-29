
import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='hetnet-v0',
    entry_point='gym_hetnet.envs:HetnetEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)

register(
    id='hetnet-naive-v0',
    entry_point='gym_hetnet.envs:HetnetNaive',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)
