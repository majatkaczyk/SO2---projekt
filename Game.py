import pygame
import random
import threading
import time

from Apple import Apple
from Poison import Poison

duck_img = pygame.image.load("assets/duck.png")
hedgehog_img = pygame.image.load("assets/hedgehog.png")
apple_img = pygame.image.load("assets/apple.png")
haps_yellow = pygame.image.load("assets/haps_yellow.png")
eaten_apple_img = pygame.image.load("assets/eaten_apple.png")
score = 0


class Game:
    def __init__(self, poison: Poison, apple: Apple, window, font):
        self.frame = pygame.rect.Rect(298, 148, 454, 454)
        self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
        self.poison = poison
        self.apple = apple
        self.window = window
        self.font = font

    def start(self):
        global score
        run = True

        while run:
            for event in pygame.event.get():
                # close the window:
                if event.type == pygame.QUIT:
                    run = False

            # add background color:
            self.window.fill((130, 30, 30))
            pygame.draw.rect(self.window, (255, 255, 255), self.frame)
            pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
            score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.window.blit(score_text, (10, 10))

            # print duck:
            self.window.blit(duck_img, (150, 300))
            self.window.blit(hedgehog_img, (750, 300))
            apple_thread = threading.Thread(target=self.apple.apple)
            poison_thread = threading.Thread(target=self.poison.poison)
            apple_thread.start()
            poison_thread.start()
            apple_thread.join()
            poison_thread.join()

            if pygame.key.get_pressed()[pygame.K_SPACE] and (
                self.apple.apple_x == 300 and self.apple.apple_y == 300
            ):
                self.duck_eats()
            if pygame.key.get_pressed()[pygame.K_SPACE] and (
                self.poison.poison_x == 300 and self.poison.poison_y == 300
            ):
                score = 0
                self.draw_game_over_screen()
                run = False
                pygame.time.wait(2000)
            pygame.display.update()

    def duck_eats(self):
        global score
        score += 1
        pygame.display.update()
        self.apple.apple_x = 300
        self.apple.apple_y = 300
        self.window.blit(apple_img, (300, 300))
        shape = pygame.rect.Rect(300, 300, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)
        self.window.blit(eaten_apple_img, (300, 300))
        # time.sleep(2)
        self.window.blit(haps_yellow, (150, 150))
        pygame.time.wait(650)

    def draw_game_over_screen(self):
        pygame.display.update()
        pygame.time.wait(650)
        self.window.fill((130, 30, 30))
        font = pygame.font.SysFont(None, 40)
        title = font.render("Game Over, you ate poison :(", True, (255, 255, 255))
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        self.window.blit(
            title, (1050 / 2 - title.get_width() / 2, 750 / 2 - title.get_height() / 3)
        )
        pygame.display.update()
