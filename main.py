import pygame
import pygame_gui
import random

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
karakter_img = pygame.image.load("karakter.png")
altin_img = pygame.image.load("altin.png")
cukur_img = pygame.image.load("cukur.png")
vampir_img = pygame.image.load("vampir.png")

# Board çizimi
def draw_board(surface):
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect((col * CELL_SIZE) + ((col + 1) * PADDING),(row * CELL_SIZE) + ((row + 1) * PADDING),CELL_SIZE,CELL_SIZE)
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
    
    
    window_surface.blit(karakter_img, ((0 * CELL_SIZE) + ((0 + 4) * PADDING), (3 * CELL_SIZE) + ((3 + 4) * PADDING)))
    
    # sol altta karakter, üstü ve sağı ise boş. Dolayısıyla geriye 13 hücre kalır.
    # 2 tane çukur, 1 tane altın ve 1 tane vampiri; birbirleriyle çakışmayacak şekilde rastgele olarak yerleştirmeli!
    konumlar = [(0,0),(0,1),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
    gorseller = [altin_img,vampir_img,cukur_img]
    
    i = 0
    while i < 3:
        rastgeleSayi = random.randint(0,len(konumlar) - 1)
        x_ekseni = konumlar[rastgeleSayi][0]
        y_ekseni = konumlar[rastgeleSayi][1]
        
        if i < 2:
            window_surface.blit(gorseller[i], ((x_ekseni * CELL_SIZE) + ((x_ekseni + 4) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 4) * PADDING)))
        else:
            window_surface.blit(gorseller[i], ((x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING)))
            konumlar.remove(konumlar[rastgeleSayi])
            
            rastgeleSayi = random.randint(0,len(konumlar) - 1)
            x_ekseni = konumlar[rastgeleSayi][0]
            y_ekseni = konumlar[rastgeleSayi][1]
            window_surface.blit(gorseller[i], ((x_ekseni * CELL_SIZE) + ((x_ekseni + 1) * PADDING), (y_ekseni * CELL_SIZE) + ((y_ekseni + 1) * PADDING)))
            
        konumlar.remove(konumlar[rastgeleSayi])
        i = i + 1


# Pygame başlat
pygame.init()

# Pencere oluştur
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wumpus World')

# UI yöneticisi oluştur
ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# Ana döngü
running = True
oyunBasladi = False
while running:
    
    #Flag mantığı ile bir kez çalıştırılması istenen kodlar, bu koşul bloğuna yazılmalır.
    if oyunBasladi == False:
        window_surface.fill(BLACK)
        draw_board(window_surface)
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window_surface)
        oyunBasladi = True
        
    #time_delta = pygame.time.Clock().tick(60) / 1000.0
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    
    pygame.display.update()

pygame.quit()