import numpy as np
import matplotlib.pyplot as plt
import gym
import random

from gym_hetnet.envs.hetnet_env import HetnetEnv

def timeToExecuteAction(state1,state2,action):
    # r(x,y,a)
    return 1

def qLearning(env, config):
    # HYPERPARAMETERS
    train_episodes = config.getint('train_episodes')    # Total train episodes
    max_steps=config.getint('max_steps')                # Max steps per episode
    alpha = config.getfloat('alpha')                    # Learning rate
    gamma = config.getfloat('gamma')                    # Discounting rate

    # EXPLORATION / EXPLOITATION PARAMETERS
    epsilon=config.getfloat("epsilon")                   # Exploration rate
    max_epsilon = config.getfloat('max_epsilon')         # Exploration probability at start
    min_epsilon = config.getfloat('min_epsilon')         # Minimum exploration probability 
    decay_rate = config.getfloat('decay_rate')           # Exponential decay rate for exploration prob

    action_size = env.action_space.n
    state_size = env.observation_space.n
    print("Action space size: ", action_size)
    print("State space size: ", state_size)

    # INITIALISE Q TABLE TO ZERO
    Q = np.zeros((state_size, action_size))
    visitas = np.zeros((state_size, action_size))

    # TRAINING PHASE
    training_rewards = []   # list of rewards

    for episode in range(train_episodes):
        if episode % 1000 == 0:
            print("Episode: ",episode,"/",train_episodes)
        state = env.reset()    # Reset the environment
        cumulative_training_rewards = 0
        
        for step in range(max_steps):
            # Choose an action (a) among the possible states (s)
            exp_exp_tradeoff = random.uniform(0, 1)   # choose a random number
            # If this number > epsilon, select the action corresponding to the biggest Q value for this state (Exploitation)
            if exp_exp_tradeoff > epsilon:
                action = np.argmax(Q[state,:])
            # Else choose a random action (Exploration)
            else:
                action = env.action_space.sample()
            
            # Perform the action (a) and observe the outcome state(s') and reward (r)
            new_state, reward, done, info = env.step(action)
            visitas[state, action] += 1

            # Update the Q table using the Bellman equation: Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]

            timeUnits = timeToExecuteAction(state, new_state, action)
            aux = np.exp(-gamma*timeUnits)
            Q[state,action] = Q[state,action] + alpha * (((1-aux)/gamma)* reward + (aux * np.max(Q[new_state, :])) - Q[state,action])

            cumulative_training_rewards += reward  # increment the cumulative reward        
            state = new_state         # Update the state
            
            # If we reach the end of the episode
            if done == True:
                print ("Cumulative reward for episode {}: {}".format(episode, cumulative_training_rewards))
                break
        
        # Reduce epsilon (because we need less and less exploration)
        epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
        
        # append the episode cumulative reward to the list
        training_rewards.append(cumulative_training_rewards)

    print ("Training score over time: " + str(sum(training_rewards)/train_episodes))

    return Q, visitas

if __name__ == "__main__":
    import configparser
    import numpy as np
    from gym_hetnet.envs.hetnet_env import HetnetEnv
    from examples.qlearning import qLearning
    import time

    config = configparser.ConfigParser()
    config.read("settings.ini")
    config_sections = config.sections()
    for experimentName in config_sections:
        settings = config[experimentName]
        print(f"Executing experiment section: {experimentName}")
        env = HetnetEnv(settings.getint("maxMacro"),settings.getint("maxFento"))

        start_time = time.time()

        Q, visitas = qLearning(env, settings)

        percent = np.count_nonzero(visitas)  / (visitas.shape[0]*visitas.shape[1])
        print("--- %s minutes ---" % ((time.time() - start_time)/60))
        print((percent * 100)," % visited\n")

    print("Process finished")

