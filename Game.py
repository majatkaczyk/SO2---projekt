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
duck_score = 0
hedgehog_score = 0
lock = threading.Lock()


class Game:
    def __init__(self, poison: Poison, apple: Apple, window, font):
        self.frame = pygame.rect.Rect(298, 148, 454, 454)
        self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
        self.poison = poison
        self.apple = apple
        self.window = window
        self.font = font

        self.semaphore = threading.Semaphore()
        self.lock = threading.Lock()

    def start(self):
        global duck_score
        global hedgehog_score
        run = True

        while run:
            for event in pygame.event.get():
                # close the window:
                if event.type == pygame.QUIT:
                    run = False

            self.draw_game()

            apple_thread = threading.Thread(target=self.apple.apple)
            poison_thread = threading.Thread(target=self.poison.poison)
            apple_thread.start()
            poison_thread.start()
            apple_thread.join()
            poison_thread.join()

            self.duck_logic()
            if duck_score < 0:
                self.draw_game_over_screen()
                run = False
                pygame.time.wait(2000)

            self.hedgehog_logic()
            if hedgehog_score < 0:
                self.draw_game_over_screen()
                run = False
                pygame.time.wait(2000)

            pygame.display.update()

    def duck_eats(self):
        self.semaphore.acquire()
        self.lock.acquire()

        global duck_score
        duck_score += 1

        pygame.display.update()

        # hide whole apple
        shape = pygame.rect.Rect(300, 300, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)

        # show eaten apple
        self.window.blit(eaten_apple_img, (300, 300))

        self.window.blit(haps_yellow, (150, 150))
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()

    def duck_poison(self):
        self.semaphore.acquire()
        self.lock.acquire()

        global duck_score
        duck_score -= 5

        # tutaj mozesz zrobic animacje itd na trucizne
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()

    def hedgehog_poison(self):
        self.semaphore.acquire()
        self.lock.acquire()

        global hedgehog_score
        hedgehog_score -= 5

        # tutaj mozesz zrobic animacje itd na trucizne
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()


    def hedgehog_eats(self):
        self.semaphore.acquire()
        self.lock.acquire()

        global hedgehog_score
        hedgehog_score += 1

        pygame.display.update()

        shape = pygame.rect.Rect(600, 300, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)

        self.window.blit(eaten_apple_img, (600, 300))

        self.window.blit(haps_yellow, (450, 150))
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()

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

    def draw_game(self):
        # add background color:
        self.window.fill((130, 30, 30))
        pygame.draw.rect(self.window, (255, 255, 255), self.frame)
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        # print score
        duck_score_text = self.font.render(
            f"Duck score: {duck_score}", True, (255, 255, 255)
        )
        self.window.blit(duck_score_text, (10, 10))

        hedgehog_score_text = self.font.render(
            f"Hedgehog score: {hedgehog_score}", True, (255, 255, 255)
        )
        self.window.blit(hedgehog_score_text, (810, 10))
        # print animals:
        self.window.blit(duck_img, (150, 300))
        self.window.blit(hedgehog_img, (750, 300))

    def duck_logic(self):
        if pygame.key.get_pressed()[pygame.K_a] and (
            self.apple.apple_x == 300 and self.apple.apple_y == 300
        ) and (
            self.poison.poison_x == 300 and self.poison.poison_y == 300
        ):
            # nothing happens
            pygame.time.wait(650)
            
        elif pygame.key.get_pressed()[pygame.K_a] and (
            self.apple.apple_x == 300 and self.apple.apple_y == 300
        ):
            self.duck_eats()

        elif pygame.key.get_pressed()[pygame.K_a] and (
            self.poison.poison_x == 300 and self.poison.poison_y == 300
        ):
            self.duck_poison()


    def hedgehog_logic(self):
        if pygame.key.get_pressed()[pygame.K_UP] and (
            self.apple.apple_x == 600 and self.apple.apple_y == 300
        ) and (
            self.poison.poison_x == 600 and self.poison.poison_y == 300
        ):
            # nothing happens
            pygame.time.wait(650)        

        elif pygame.key.get_pressed()[pygame.K_UP] and (
            self.apple.apple_x == 600 and self.apple.apple_y == 300
        ):
            self.hedgehog_eats()
        elif pygame.key.get_pressed()[pygame.K_UP] and (
            self.poison.poison_x == 600 and self.poison.poison_y == 300
        ):
            self.hedgehog_poison()
