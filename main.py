import pygame

pygame.init()
window = pygame.display.set_mode((1050, 750))

duckImg = pygame.image.load('kaczuszka.png')

def duck():
    window.blit(duckImg, (150, 300))

# create first tile:
frame = pygame.rect.Rect(298, 148, 454, 454)
tile1 = pygame.rect.Rect(300, 150, 150, 150)
tile2 = pygame.rect.Rect(450, 150, 150, 150)
tile3 = pygame.rect.Rect(600, 150, 150, 150)
tile4 = pygame.rect.Rect(300, 300, 150, 150)
tile5 = pygame.rect.Rect(450, 300, 150, 150)
tile6 = pygame.rect.Rect(600, 300, 150, 150)
tile7 = pygame.rect.Rect(300, 450, 150, 150)
tile8 = pygame.rect.Rect(450, 450, 150, 150)
tile9 = pygame.rect.Rect(600, 450, 150, 150)

# main loop:
run = True
while run:
    for event in pygame.event.get():
        # close the window:
        if event.type == pygame.QUIT:
            run = False

    # add background color:
    window.fill((130, 30, 30))
    duck()

    # draw tile1 [window, color, object]
    pygame.draw.rect(window, (255,255,255), frame)
    pygame.draw.rect(window, (120,0,0), tile1)
    pygame.draw.rect(window, (190,0,0), tile2)
    pygame.draw.rect(window, (255,0,0), tile3)
    pygame.draw.rect(window, (0,120,0), tile4)
    pygame.draw.rect(window, (0,190,0), tile5)
    pygame.draw.rect(window, (0,255,0), tile6)
    pygame.draw.rect(window, (0,0,120), tile7)
    pygame.draw.rect(window, (0,0,190), tile8)
    pygame.draw.rect(window, (0,0,255), tile9)
    pygame.display.update()