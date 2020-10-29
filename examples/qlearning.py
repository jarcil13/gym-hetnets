import gym

def qLearning(env):
    currentState = env.reset()
    while True:
        action = policy(currentState)               # Exploitation
        if np.random.random() < explorationRate(i): # Exploration
            action = env.action_space.sample()      # Explora una acción cualquiera

        newState, reward, done, info = env.step(action)   # Cambiar de estado

        if done:
            print("Finished Iteration ",i)
            break

        # Update Q-Table
        lr = learningRate(i)
        learnt_value = updateQ(reward, newState)
        oldValue = Qtable[currentState][action]
        newValue = Qtable[currentState][action] = ( lr * newValue )  +  ( (1-lr) * oldValue )
        currentState = newState
        
if __name__ == "__main__": 
    env = gym.make('gym_hetnet:hetnet-v0')
    iter = 10
    for i in range(iter):
        qLearning(env)
    env.close()
