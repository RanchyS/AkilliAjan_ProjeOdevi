import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


#oyun alanından o anki durum verilerinin alınması
def durum_verileri(karakter_pos, altin_pos, vampir_pos, cukur1_pos, cukur2_pos):
    durum = np.zeros((BOARD_SIZE, BOARD_SIZE))
    durum[karakter_pos] = 1  
    durum[altin_pos] = 2  
    durum[vampir_pos] = -1  # wumpus
    durum[cukur1_pos] = -2  
    durum[cukur2_pos] = -2  
    return durum


# Eylemler
eylemler = ["up", "down", "left", "right"]

#aksiyonların rastgeleliğinin sağlanması
def aksiyon_sec(durum, epsilon):
    if random.random() < epsilon:
        return random.choice(eylemler)
    else:
        with torch.no_grad():
            q_degerleri = model(torch.tensor(durum, dtype=torch.float32).flatten())

            #en yüksek q değeri
            return eylemler[torch.argmax(q_degerleri).item()]

# Modeli başlat
class DQN(nn.Module):

    #nöral katmanların sağlanması
    def _init_(self, input_size, output_size):
        super(DQN, self)._init_()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )
    #girdiyi katmanlardan geçirme
    def forward(self, x):
        return self.fc(x)
# Modeli başlat
input_size = BOARD_SIZE * BOARD_SIZE
output_size = len(eylemler)
model = DQN(input_size, output_size)
target_model = DQN(input_size, output_size)
target_model.load_state_dict(model.state_dict())
target_model.eval()

#öğrenme oranı ve optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)


# Deneyim belleği
memory = deque(maxlen=10000)
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
batch_size = 64

def update_memory(state, action, next_state, reward):
    memory.append((state, action, next_state, reward))

def update_model():
    if len(memory) < batch_size:
        return

    batch = random.sample(memory, batch_size)
    states, actions, next_states, rewards = zip(*batch)

    states = torch.tensor(states, dtype=torch.float32)
    actions = torch.tensor(actions, dtype=torch.long)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    next_states = torch.tensor(next_states, dtype=torch.float32)

    q_values = model(states.flatten(start_dim=1))
    next_q_values = target_model(next_states.flatten(start_dim=1)).max(1)[0].detach()
    target_q_values = rewards + gamma * next_q_values

    loss = nn.functional.mse_loss(q_values.gather(1, actions.unsqueeze(1)), target_q_values.unsqueeze(1))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epsilon > min_epsilon:
        epsilon *= epsilon_decay

num_episodes = 1000

for episode in range(num_episodes):
    env = WumpusWorld()
    state = get_state(env.character_position, env.gold_position, env.wumpus_position, env.pit1_position, env.pit2_position).flatten()
    done = False
    total_reward = 0

    while not done:
        action = select_action(state, epsilon)
        reward_message = env.take_action(action)
        reward = 0

        if reward_message == "Congratulations! You found the gold and returned safely!":
            reward = 100
            done = True
        elif reward_message == "Game Over! Wumpus caught you!" or reward_message == "Game Over! You fell into a pit!":
            reward = -100
            done = True
        else:
            reward = -1

        next_state = get_state(env.character_position, env.gold_position, env.wumpus_position, env.pit1_position, env.pit2_position).flatten()
        update_memory(state, action, next_state, reward)
        update_model()

        state = next_state
        total_reward += reward

    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

    if (episode + 1) % 10 == 0:
        target_model.load_state_dict(model.state_dict())

