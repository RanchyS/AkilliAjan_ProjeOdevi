import gym
from gym import spaces
import numpy as np
import random
import pygame

class WumpusWorldEnv(gym.Env):
    def __init__(self):
        super(WumpusWorldEnv, self).__init__()
        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right
        self.observation_space = spaces.Box(low=0, high=3, shape=(2,), dtype=np.int32)
        
        # Pygame initialization
        self.BOARD_SIZE = 4
        self.CELL_SIZE = 120
        self.PADDING = 10
        self.WINDOW_WIDTH = self.BOARD_SIZE * self.CELL_SIZE + (self.BOARD_SIZE + 1) * self.PADDING
        self.WINDOW_HEIGHT = self.BOARD_SIZE * self.CELL_SIZE + (self.BOARD_SIZE + 1) * self.PADDING
        self.init_pygame()
        
        self.reset()
        
    def init_pygame(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.karakter_img = pygame.image.load("images/karakter.png")
        self.altin_img = pygame.image.load("images/altin.png")
        self.cukur_img = pygame.image.load("images/cukur.png")
        self.cukur2_img = pygame.image.load("images/cukur2.png")
        self.vampir_img = pygame.image.load("images/vampir.png")
    
    def reset(self):
        self.karakterX = 0
        self.karakterY = 3
        self.state = np.array([self.karakterX, self.karakterY])
        self.done = False
        
        self.konumlar = [(0,0),(0,1),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
        
        altinKonumu = random.randint(0, 3)
        if altinKonumu == 0:
            self.altin = (1, 1)
        elif altinKonumu == 1:
            self.altin = (1, 2)
        elif altinKonumu == 2:
            self.altin = (2, 1)
        else:
            self.altin = (2, 2)
        
        self.konumlar.remove(self.altin)
        
        self.vampir = random.choice(self.konumlar)
        self.konumlar.remove(self.vampir)
        
        self.cukur1 = random.choice(self.konumlar)
        self.konumlar.remove(self.cukur1)
        
        self.cukur2 = random.choice(self.konumlar)
        self.konumlar.remove(self.cukur2)
        
        return self.state

    def step(self, action):
        if action == 0 and self.karakterY != 0:  # Up
            self.karakterY -= 1
        elif action == 1 and self.karakterY != 3:  # Down
            self.karakterY += 1
        elif action == 2 and self.karakterX != 0:  # Left
            self.karakterX -= 1
        elif action == 3 and self.karakterX != 3:  # Right
            self.karakterX += 1

        self.state = np.array([self.karakterX, self.karakterY])
        
        if (self.karakterX, self.karakterY) == self.altin:
            reward = 100
            self.done = True
        elif (self.karakterX, self.karakterY) in [self.vampir, self.cukur1, self.cukur2]:
            reward = -100
            self.done = True
        else:
            reward = -1
        
        return self.state, reward, self.done, {}

    def render(self):
        self.window_surface.fill((0, 0, 0))
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                rect = pygame.Rect((col * self.CELL_SIZE) + ((col + 1) * self.PADDING), (row * self.CELL_SIZE) + ((row + 1) * self.PADDING), self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.window_surface, (255, 255, 255), rect)
                pygame.draw.rect(self.window_surface, (0, 0, 0), rect, 2)

        self.window_surface.blit(self.karakter_img, (self.karakterX * self.CELL_SIZE + (self.karakterX + 1) * self.PADDING, self.karakterY * self.CELL_SIZE + (self.karakterY + 1) * self.PADDING))
        self.window_surface.blit(self.altin_img, (self.altin[0] * self.CELL_SIZE + (self.altin[0] + 1) * self.PADDING, self.altin[1] * self.CELL_SIZE + (self.altin[1] + 1) * self.PADDING))
        self.window_surface.blit(self.vampir_img, (self.vampir[0] * self.CELL_SIZE + (self.vampir[0] + 1) * self.PADDING, self.vampir[1] * self.CELL_SIZE + (self.vampir[1] + 1) * self.PADDING))
        self.window_surface.blit(self.cukur_img, (self.cukur1[0] * self.CELL_SIZE + (self.cukur1[0] + 1) * self.PADDING, self.cukur1[1] * self.CELL_SIZE + (self.cukur1[1] + 1) * self.PADDING))
        self.window_surface.blit(self.cukur2_img, (self.cukur2[0] * self.CELL_SIZE + (self.cukur2[0] + 1) * self.PADDING, self.cukur2[1] * self.CELL_SIZE + (self.cukur2[1] + 1) * self.PADDING))

        pygame.display.flip()
