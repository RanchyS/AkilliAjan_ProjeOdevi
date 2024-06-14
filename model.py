import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


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

class DQN(nn.Module):
    def _init_(self, input_size, output_size):
        super(DQN, self)._init_()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )
    
    def forward(self, x):
        return self.fc(x)
# Modeli başlat
input_size = BOARD_SIZE * BOARD_SIZE
output_size = len(eylemler)
model = DQN(input_size, output_size)
target_model = DQN(input_size, output_size)
target_model.load_state_dict(model.state_dict())
target_model.eval()

optimizer = optim.Adam(model.parameters(), lr=0.001)