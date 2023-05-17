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
eaten_poison_img = pygame.image.load("assets/eaten_poison.png")
duck_game_over_img = pygame.image.load("assets/duck_win.png")
hedgehog_game_over_img = pygame.image.load("assets/hedgehog_win.png")
duck_score = 0
hedgehog_score = 0


class Game:
    def __init__(self, poison: Poison, apple: Apple, window, font):
        self.frame = pygame.rect.Rect(298, 148, 454, 454)
        self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
        self.poison = poison
        self.apple = apple
        self.window = window
        self.font = font
        self.game_state = "start_screen"
        self.game_height = 750
        self.game_width = 1050

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

            if self.game_state == "start_screen":
                self.draw_start_screen()
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.game_state = "game_started"

            if self.game_state == "game_started":
                self.draw_game()

                apple_thread = threading.Thread(target=self.apple.apple)
                poison_thread = threading.Thread(target=self.poison.poison)
                apple_thread.start()
                poison_thread.start()
                apple_thread.join()
                poison_thread.join()

                self.duck_logic()
                if duck_score < 0:
                    self.draw_game_over_screen("Hedgehog wins!", 2.1)
                    run = False
                    pygame.time.wait(2000)

                self.hedgehog_logic()
                if hedgehog_score < 0:
                    self.draw_game_over_screen("Duck wins!", 1.95)
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

        pygame.display.update()

        # hide whole poison
        shape = pygame.rect.Rect(300, 300, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)

        # show eaten poison
        self.window.blit(eaten_poison_img, (300, 300))

        self.window.blit(haps_yellow, (150, 150))
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()

    def hedgehog_poison(self):
        self.semaphore.acquire()
        self.lock.acquire()

        global hedgehog_score
        hedgehog_score -= 5

        pygame.display.update()

        shape = pygame.rect.Rect(600, 300, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)

        self.window.blit(eaten_poison_img, (600, 300))

        self.window.blit(haps_yellow, (750, 150))

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

        self.window.blit(haps_yellow, (750, 150))
        pygame.time.wait(650)

        self.lock.release()
        self.semaphore.release()

    def draw_game_over_screen(self, text, part_width):
        pygame.display.update()
        pygame.time.wait(850)
        self.window.fill((130, 30, 30))
        font = pygame.font.SysFont(None, 40)
        title = font.render("GAME OVER", True, (255, 255, 255))
        subtitle = font.render(text, True, (255, 255, 255))
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        self.window.blit(
            title,
            (
                self.game_width / 2 - title.get_width() / 2,
                self.game_height / 5 - title.get_height() / 3,
            ),
        )
        self.window.blit(
            subtitle,
            (
                self.game_width / part_width - title.get_width() / 2,
                self.game_height / 4 - title.get_height() / 3,
            ),
        )
        self.window.blit(duck_game_over_img, (300, 300))
        self.window.blit(hedgehog_game_over_img, (600, 300))

        duck_score_text = self.font.render(
            f"Duck score: {duck_score}", True, (255, 255, 255)
        )
        self.window.blit(duck_score_text, (300, 460))

        hedgehog_score_text = self.font.render(
            f"Hedgehog score: {hedgehog_score}", True, (255, 255, 255)
        )
        self.window.blit(hedgehog_score_text, (600, 460))

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
        if (
            pygame.key.get_pressed()[pygame.K_a]
            and (self.apple.apple_x == 300 and self.apple.apple_y == 300)
            and (self.poison.poison_x == 300 and self.poison.poison_y == 300)
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
        if (
            pygame.key.get_pressed()[pygame.K_UP]
            and (self.apple.apple_x == 600 and self.apple.apple_y == 300)
            and (self.poison.poison_x == 600 and self.poison.poison_y == 300)
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

    def draw_start_screen(self):
        self.window.fill((130, 30, 30))
        font = pygame.font.SysFont(None, 40)
        title = font.render("Hungry Hippos,", True, (255, 255, 255))
        subtitle = font.render(
            "but hippos are duck and hedgehog", True, (255, 255, 255)
        )
        start_button = font.render("Press space to start", True, (255, 255, 255))
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        self.window.blit(
            title,
            (
                self.game_width / 2 - title.get_width() / 2,
                self.game_height / 5 - title.get_height() / 3,
            ),
        )
        self.window.blit(
            subtitle,
            (
                self.game_width / 2.75 - title.get_width() / 2,
                self.game_height / 4 - title.get_height() / 3,
            ),
        )
        self.window.blit(
            start_button,
            (
                self.game_width / 2 - start_button.get_width() / 2,
                self.game_height / 2 + start_button.get_height() / 2,
            ),
        )
        pygame.display.update()
