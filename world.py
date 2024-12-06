import pygame
import random
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
#import random
import torch
from torch import nn
import torch.nn.functional as F
from wumpus import *
import pyautogui

### entegrasyon

desc = np.array([["F","F","F","F"],
                ["F","F","F","F"],
                ["F","F","F","F"],
                ["S","F","F","F"]])


###

# Board boyutları
BOARD_SIZE = 4
CELL_SIZE = 120
PADDING = 10

# Renkler

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pencere boyutları
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE + 1) * PADDING
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE + 1) * PADDING

# Görseller
karakter_img = pygame.image.load("images/karakter.png")
altin_img = pygame.image.load("images/altin.png")
cukur_img = pygame.image.load("images/cukur.png")
cukur2_img = pygame.image.load("images/cukur2.png")
vampir_img = pygame.image.load("images/vampir.png")

gorseller = dict() # bütün öğelerin indisini tutar

# karakterin başlangıç aşamasındaki yeri rastgele olarak belirlenmiyor, dolayısıyla:

karakterX = 0
karakterY = 3

# Rastgeleliğin sağlanması

# sol altta karakter, üstü ve sağı ise boş. Dolayısıyla geriye 13 hücre kalır.
# 2 tane çukur, 1 tane altın ve 1 tane vampiri; birbirleriyle çakışmayacak şekilde rastgele olarak yerleştirmeli!
konumlar = [(0,0),(0,1),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]

##
altin_cukur = [0,1,2,3]
##

altinKonumu = random.randint(0,3) # altını, {(1,1),(1,2),(2,1),(2,2)} konumlarından birinde oluşturma
x_ekseni = 0
y_ekseni = 0
if altinKonumu == 0:
    x_ekseni = 1
    y_ekseni = 1
elif altinKonumu == 1:
    x_ekseni = 1
    y_ekseni = 2
elif altinKonumu == 2:
    x_ekseni = 2
    y_ekseni = 1
else:
    x_ekseni = 2
    y_ekseni = 2

gorseller[altin_img] = (x_ekseni,y_ekseni)
konumlar.remove((x_ekseni,y_ekseni)) # çakışmayı önlemek için
altin_cukur.remove(altinKonumu)

## 

cukur2Konumu = altin_cukur[random.randint(0,2)] # cukur2'yi, {(1,1),(1,2),(2,1),(2,2)} konumlarından birinde, altınla çakıştırmadan oluşturma
x_ekseni = 0
y_ekseni = 0
if cukur2Konumu == 0:
    x_ekseni = 1
    y_ekseni = 1
elif cukur2Konumu == 1:
    x_ekseni = 1
    y_ekseni = 2
elif cukur2Konumu == 2:
    x_ekseni = 2
    y_ekseni = 1
else:
    x_ekseni = 2
    y_ekseni = 2

gorseller[cukur2_img] = (x_ekseni,y_ekseni)
konumlar.remove((x_ekseni,y_ekseni)) # çakışmayı önlemek için

i = 0
while i < 2:
    rastgeleSayi = random.randint(0,len(konumlar) - 1)
    x_ekseni = konumlar[rastgeleSayi][0]
    y_ekseni = konumlar[rastgeleSayi][1]
        
    if i == 0:
        gorseller[vampir_img] = (x_ekseni,y_ekseni)
        
    else:
        gorseller[cukur_img] = (x_ekseni,y_ekseni)
        
        #konumlar.remove(konumlar[rastgeleSayi])
            
        #rastgeleSayi = random.randint(0,len(konumlar) - 1)
        #x_ekseni = konumlar[rastgeleSayi][0]
        #x_ekseni = konumlar[rastgeleSayi][1]
        #gorseller[cukur2_img] = (x_ekseni,y_ekseni)
            
    konumlar.remove(konumlar[rastgeleSayi])
    i = i + 1


### rastgele oluşturulan haritanın, desc değişkeni üzerine kaydedilmesi

altin_flag = True

def degerAta(gorsel_x,gorsel_y):
    global altin_flag
    if altin_flag:
        desc[gorsel_x][gorsel_y] = "G"
        altin_flag = False
    else:
        desc[gorsel_x][gorsel_y] = "H"

for (gorsel_y,gorsel_x) in gorseller.values():
    if gorsel_y == 0 and gorsel_x == 0:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 0 and gorsel_x == 1:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 1 and gorsel_x == 0:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 1 and gorsel_x == 1:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 1 and gorsel_x == 2:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 2 and gorsel_x == 0:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 2 and gorsel_x == 1:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 2 and gorsel_x == 2:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 2 and gorsel_x == 3:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 3 and gorsel_x == 0:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 3 and gorsel_x == 1:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 3 and gorsel_x == 2:
        degerAta(gorsel_x,gorsel_y)
        
    if gorsel_y == 3 and gorsel_x == 3:
        degerAta(gorsel_x,gorsel_y) 
    
print(desc)

###

### sınıflar arası baş

agent = FrozenLakeDQL()
is_slippery = False
agent.train(1000, is_slippery=is_slippery, desc = desc) # If you train your agent once, you don't need to run this line again!
agent.test(0, is_slippery=is_slippery, desc = desc) # but in this project, we generate a random map every time so you have to run that line!

best_actions_updated = list(range(16))
if len(best_actions) > 16:
    i = len(best_actions)
    sayac = 0
    while(i>16):
        best_actions_updated[16 - 1 - sayac] = best_actions[i - 1]
        sayac += 1
        i -= 1
else:
    best_actions_updated  = best_actions

print(best_actions_updated)


### son

# Karakterin ızgara üzerinde hareket ettirilmesi

duvaraCarptiMi = "NOPE"

def karakterHareketi(key):
    global karakterX
    global karakterY
    global duvaraCarptiMi
    global offsetX
    global offsetY
    
    adim_snd.play()
    if key == pygame.K_UP and karakterY != 0:
        karakterY -= 1 # 1 indisi ile y ekseni nitelenir!
        adim_snd.play() 
    elif key == pygame.K_DOWN and karakterY != 3:
        karakterY += 1
        adim_snd.play()
    elif key == pygame.K_LEFT and karakterX != 0:
        karakterX -= 1 # 0 indisi ile x ekseni nitelenir!
        adim_snd.play()
    elif key == pygame.K_RIGHT and karakterX != 3:
        karakterX += 1
        adim_snd.play()
    else:
        # animasyon
        duvaraCarpma_snd.play()
        if key == pygame.K_UP and karakterY == 0:
            offsetX = 3.75
            offsetY = 1.25
            duvaraCarptiMi = "UP"
        elif key == pygame.K_DOWN and karakterY == 3:
            offsetX = 3.75
            offsetY = 6.5
            duvaraCarptiMi = "DOWN"
               
        elif key == pygame.K_RIGHT and karakterX == 3:
            offsetX = 6.75
            offsetY = 4
            duvaraCarptiMi = "RIGHT"
            
        elif key == pygame.K_LEFT and karakterX == 0:
            offsetX = 0.75
            offsetY = 4
            duvaraCarptiMi = "LEFT"
            
        
offsetX = 3.75
offsetY = 4

    
# Board çizimi
def draw_board(surface):
    global duvaraCarptiMi
    global offsetX
    global offsetY
    global sesIcinBayrak
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect((col * CELL_SIZE) + ((col + 1) * PADDING),(row * CELL_SIZE) + ((row + 1) * PADDING),CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
    
    #sabit görsellerin ızgaraya eklenmesi
    for (gorsel,(x_ekseni,y_ekseni)) in gorseller.items():
        if gorsel == altin_img:
            window_surface.blit(gorsel, ((x_ekseni * CELL_SIZE) + ((x_ekseni + 4) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 4) * PADDING)))
        elif gorsel == vampir_img:
            window_surface.blit(gorsel, ((x_ekseni * CELL_SIZE) + ((x_ekseni + 3.75) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 3) * PADDING)))
        elif gorsel == cukur_img:
            window_surface.blit(gorsel, ((x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING)))
        elif gorsel == cukur2_img:
            window_surface.blit(gorsel, ((x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING)))
    
    oyunDurumu = oyun_Durumu()
    if oyunDurumu != "Devam Ediyor":
        
        if oyunDurumu == "Oyun kazanıldı!":
            text_surface = test_font.render('AJAN BASARDI!', False, 'Green')
            window_surface.blit(text_surface,(50,235))
            if sesIcinBayrak:
                kazanma_snd.play()
                sesIcinBayrak = False
        else:
            text_surface = test_font.render('AJAN BASARAMADI!', False, 'Red')
            window_surface.blit(text_surface,(0,235))
            if sesIcinBayrak:
                kaybetme_snd.play()
                sesIcinBayrak = False
    
    # karakter hareketinin gösterilmesi
    window_surface.blit(karakter_img, ((karakterX * CELL_SIZE) + ((karakterX + offsetX) * PADDING), (karakterY * CELL_SIZE) + ((karakterY + offsetY) * PADDING)))

# Oyun durumu inceleme
def oyun_Durumu():
    oyunDurumu = "Devam Ediyor"
    for (gorsel,(x,y)) in gorseller.items():
        if karakterX == x and karakterY == y:
            if gorsel == altin_img:
                oyunDurumu = "Oyun kazanıldı!"
            else:
                oyunDurumu = "Oyun kaybedildi!"
    return oyunDurumu
        
### oto-tuslama

tuslamalar = best_actions_updated # \0 yerleştirme nedenim: oyunun başlangıç durumunun da gösterilmesini istemem.

tusSayac = 0
baslangicIndis = 12
baslangicDurumuGoster = True
def otomatikTuslama():
    global baslangicIndis
    global baslangicDurumuGoster

    if baslangicDurumuGoster:
        pyautogui.press('\0')
        baslangicDurumuGoster = False
    else:
        tus = tuslamalar[baslangicIndis]
        print(tus)
        if tus == "L":
            pyautogui.press('left')
            baslangicIndis -= 1
        elif tus == "R":
            pyautogui.press('right')
            baslangicIndis += 1
        elif tus == "D":
            pyautogui.press('down')
            baslangicIndis += 3
        elif tus == "U":
            pyautogui.press('up')
            baslangicIndis -= 4
    

###

# Pygame başlat
pygame.init()

# Pencere oluştur
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window_surface.fill(BLACK)
pygame.display.set_caption('Wumpus World')

# Sesler
kazanma_snd = pygame.mixer.Sound("sounds/kazanma.wav")
#kazanma_snd.set_volume(0.5)
kaybetme_snd = pygame.mixer.Sound("sounds/kaybetme.wav")
#kaybetme_snd.set_volume(0.5)
adim_snd = pygame.mixer.Sound("sounds/adim.flac")
#adim_snd.set_volume(0.5)
duvaraCarpma_snd = pygame.mixer.Sound("sounds/duvaraCarpma.mp3")

# Sonuç ekranı
test_font = pygame.font.Font("fonts/pixelType.ttf",100)

# Ana döngü
running = True
clock = pygame.time.Clock()
sesIcinBayrak = True
beyniYerineGelsinBayrak = True
while running:

    oyunDurumu = oyun_Durumu()
    
    if tusSayac < 17 and oyunDurumu == "Devam Ediyor":
        otomatikTuslama()
        tusSayac += 1     

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and oyunDurumu == "Devam Ediyor":
            if event.key in [pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT]:
                karakterHareketi(event.key)

    draw_board(window_surface)
    pygame.display.update()         

    if duvaraCarptiMi != "NOPE":
        pygame.time.wait(250)
        offsetX = 3.75
        offsetY = 4
        duvaraCarptiMi = "NOPE"
    else:
        if beyniYerineGelsinBayrak:
            pygame.time.wait(1000) # başlangıç durumunu da gösterebilmek adına \0 karakteri basıldıktan sonra 1 saniye bekle
            beyniYerineGelsinBayrak = False
        else:
            pygame.time.wait(1000) # her tuş basıldığında 1 saniye bekle
        
    clock.tick(60) # oyunun fps'ini niteler

pygame.quit() # animasyonu iyileştirebilirsin! # kara büyü(parametre = 0 olması) # vampir görünmüyor haritada