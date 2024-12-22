from training_an_agent import *

import pygame
import random
import numpy as np
import pyautogui

### entegrasyon
bulunulan_durum = baslangic_durumu
matris_boyutu = 4 # görselleştirme işlemi yalnızca 4x4 için yapıldı!
durum_matrisi = np.zeros((matris_boyutu,matris_boyutu),dtype=str)
durum_matrisi[:] = "F"
durum_matrisi[baslangic_durumu] = "S"
q_table = q_table_olusturma(matris_boyutu)
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
karakter_img = pygame.image.load("assets/images/karakter.png")
altin_img = pygame.image.load("assets/images/altin.png")
cukur_img = pygame.image.load("assets/images/cukur.png")
cukur2_img = pygame.image.load("assets/images/cukur2.png")
vampir_img = pygame.image.load("assets/images/vampir.png")

gorseller = dict() # bütün öğelerin indisini tutar

# Rastgeleliğin sağlanması

# sol altta karakter, üstü ve sağı ise boş. Dolayısıyla geriye 13 hücre kalır.
# 2 tane çukur, 1 tane altın ve 1 tane vampiri; birbirleriyle çakışmayacak şekilde rastgele olarak yerleştirmeli!
konumlar = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,2),(3,3)]

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
        durum_matrisi[gorsel_x][gorsel_y] = "G"
        altin_flag = False
    else:
        durum_matrisi[gorsel_x][gorsel_y] = "H"

for (gorsel_x,gorsel_y) in gorseller.values():
    degerAta(gorsel_x,gorsel_y)
    
print(durum_matrisi)

###

### sınıflar arası baş
matris_guncelle(durum_matrisi)
train(1000)
best_actions_updated = optimal_yolu_dondur(matris_boyutu)
print(best_actions_updated)

### son buradan kes

# Karakterin ızgara üzerinde hareket ettirilmesi

duvaraCarptiMi = "NOPE"

def karakterHareketi(key):
    global duvaraCarptiMi
    global offsetX
    global offsetY
    global bulunulan_durum

    adim_snd.play()
    if key == pygame.K_UP and bulunulan_durum[0] != 0:
        bulunulan_durum = (bulunulan_durum[0]-1,bulunulan_durum[1]) # 1 indisi ile y ekseni nitelenir!
        adim_snd.play() 
    elif key == pygame.K_DOWN and bulunulan_durum[0] != matris_boyutu - 1:
        bulunulan_durum = (bulunulan_durum[0]+1,bulunulan_durum[1])
        adim_snd.play()
    elif key == pygame.K_LEFT and bulunulan_durum[1] != 0:
        bulunulan_durum = (bulunulan_durum[0],bulunulan_durum[1]-1) # 0 indisi ile x ekseni nitelenir!
        adim_snd.play()
    elif key == pygame.K_RIGHT and bulunulan_durum[1] != matris_boyutu - 1:
        bulunulan_durum = (bulunulan_durum[0],bulunulan_durum[1]+1)
        adim_snd.play()
    else:
        # animasyon
        duvaraCarpma_snd.play()
        if key == pygame.K_UP and bulunulan_durum[0] == 0:
            offsetX = 3.75
            offsetY = 1.25
            duvaraCarptiMi = "UP"
        elif key == pygame.K_DOWN and bulunulan_durum[0] == matris_boyutu - 1:
            offsetX = 3.75
            offsetY = 6.5
            duvaraCarptiMi = "DOWN"
               
        elif key == pygame.K_RIGHT and bulunulan_durum[1] == matris_boyutu - 1:
            offsetX = 6.75
            offsetY = 4
            duvaraCarptiMi = "RIGHT"
            
        elif key == pygame.K_LEFT and bulunulan_durum[1] == 0:
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
            window_surface.blit(gorsel, ((y_ekseni * CELL_SIZE) + ((y_ekseni + 4) * PADDING), (x_ekseni * CELL_SIZE) + ((x_ekseni + 4) * PADDING)))
        elif gorsel == vampir_img:
            window_surface.blit(gorsel, ((y_ekseni * CELL_SIZE) + ((y_ekseni + 3.75) * PADDING), (x_ekseni * CELL_SIZE) + ((x_ekseni + 3) * PADDING)))
        elif gorsel == cukur_img:
            window_surface.blit(gorsel, ((y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING), (x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING)))
        elif gorsel == cukur2_img:
            window_surface.blit(gorsel, ((y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING), (x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING)))
    
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
    window_surface.blit(karakter_img, ((bulunulan_durum[1] * CELL_SIZE) + ((bulunulan_durum[1] + offsetX) * PADDING), (bulunulan_durum[0] * CELL_SIZE) + ((bulunulan_durum[0] + offsetY) * PADDING)))

# Oyun durumu inceleme
def oyun_Durumu():
    oyunDurumu = "Devam Ediyor"
    for (gorsel,(x,y)) in gorseller.items():
        if bulunulan_durum[0] == x and bulunulan_durum[1] == y:
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
            baslangicIndis += 4
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
kazanma_snd = pygame.mixer.Sound("assets/sounds/kazanma.wav")
#kazanma_snd.set_volume(0.5)
kaybetme_snd = pygame.mixer.Sound("assets/sounds/kaybetme.wav")
#kaybetme_snd.set_volume(0.5)
adim_snd = pygame.mixer.Sound("assets/sounds/adim.flac")
#adim_snd.set_volume(0.5)
duvaraCarpma_snd = pygame.mixer.Sound("assets/sounds/duvaraCarpma.mp3")

# Sonuç ekranı
test_font = pygame.font.Font("assets/fonts/pixelType.ttf",100)

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

pygame.quit()
