from dqn_agent import DQNAgent
from wumpus_env import WumpusWorldEnv
import numpy as np
import pygame

env = WumpusWorldEnv()
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)
agent.model.load_weights("dqn_model.h5")

for e in range(10):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    for time in range(500):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        
        env.render()  # Oyun alanını render et
        
        state = next_state
        if done:
            print(f"Test Episode: {e}/10, score: {time}")
            break
        
    pygame.time.wait(1000)  # Bir sonraki episode başlamadan önce bekle

pygame.quit()
