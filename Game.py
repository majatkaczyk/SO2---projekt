import pygame
import random
import threading
import time

from Apple import Apple
from Poison import Poison

# load pet images
duck_img = pygame.image.load("assets/duck.png")
hedgehog_img = pygame.image.load("assets/hedgehog.png")
dog_img = pygame.image.load("assets/dog.png")
hamster_img = pygame.image.load("assets/hamster.png")

# load food images
apple_img = pygame.image.load("assets/apple.png")
haps_yellow = pygame.image.load("assets/haps_yellow.png")
eaten_apple_img = pygame.image.load("assets/eaten_apple.png")
eaten_poison_img = pygame.image.load("assets/eaten_poison.png")

# load pets images for start and game over screen
duck_screen_img = pygame.image.load("assets/duck_win.png")
hedgehog_screen_img = pygame.image.load("assets/hedgehog_win.png")


duck_and_dog_score = 0  # first team - dog and duck
hedgehog_and_hamster_score = 0  # second team - hedgehog and hamster


class Game:
    def __init__(self, poison: Poison, apple: Apple, window, font):
        # create game board
        self.frame = pygame.rect.Rect(0, 0, 0, 0)
        self.background_tile = pygame.rect.Rect(0, 0, 0, 0)
        self.poison = poison
        self.apple = apple
        self.window = window
        self.font = font
        self.game_state = "start_screen"
        self.game_height = 750
        self.game_width = 1050

        # add semaphore and lock
        self.semaphore = threading.Semaphore()
        self.lock = threading.Lock()

    # start game
    def start(self):
        run = True

        while run:
            for event in pygame.event.get():
                # close the window:
                if event.type == pygame.QUIT:
                    run = False

            # draw start screen
            if self.game_state == "start_screen":
                self.draw_start_screen()
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.game_state = "game_started"

            # if space pressed draw game board

            # create game board

            if self.game_state == "game_started":
                self.frame = pygame.rect.Rect(298, 148, 454, 454)
                self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
                self.draw_game()

                apple_thread = threading.Thread(target=self.apple.apple)
                poison_thread = threading.Thread(target=self.poison.poison)
                apple_thread.start()
                poison_thread.start()
                apple_thread.join()
                poison_thread.join()

                self.duck_logic()
                if duck_and_dog_score < 0:
                    self.draw_game_over_screen("Hedgehog wins!", 2.1)
                    run = False
                    pygame.time.wait(2000)

                self.hedgehog_logic()
                if hedgehog_and_hamster_score < 0:
                    self.draw_game_over_screen("Duck wins!", 1.95)
                    run = False
                    pygame.time.wait(2000)

                pygame.display.update()

    def duck_eats(self, score, img):
        self.semaphore.acquire()
        self.lock.acquire()

        global duck_and_dog_score
        duck_and_dog_score += score

        pygame.display.update()

        self.draw_eaten_food(img, 300, 300)
        self.window.blit(haps_yellow, (150, 100))
        pygame.time.wait(1200)

        self.lock.release()
        self.semaphore.release()

    def hedgehog_eats(self, score, img):
        self.semaphore.acquire()
        self.lock.acquire()

        global hedgehog_and_hamster_score
        hedgehog_and_hamster_score += score

        pygame.display.update()

        self.draw_eaten_food(img, 600, 300)
        self.window.blit(haps_yellow, (750, 100))
        pygame.time.wait(1200)

        self.lock.release()
        self.semaphore.release()

    def draw_eaten_food(self, img, x_pos, y_pos):
        # hide whole food
        shape = pygame.rect.Rect(x_pos, y_pos, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)
        # show eaten food
        self.window.blit(img, (x_pos, y_pos))

    def draw_game_over_screen(self, text, part_width):
        pygame.display.update()
        pygame.time.wait(1000)
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
        self.window.blit(duck_screen_img, (300, 300))
        self.window.blit(hedgehog_screen_img, (600, 300))

        self.show_score("Duck score", 300, 460, duck_and_dog_score)
        self.show_score("Hedgehog score", 600, 460, hedgehog_and_hamster_score)

        pygame.display.update()

    def show_score(self, text, x_pos, y_pos, score):
        score_text = self.font.render(f"{text}: {score}", True, (255, 255, 255))
        self.window.blit(score_text, (x_pos, y_pos))

    def draw_game(self):
        # add background color:
        self.window.fill((130, 30, 30))
        pygame.draw.rect(self.window, (255, 255, 255), self.frame)
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        # print score
        self.show_score("Duck score", 10, 10, duck_and_dog_score)
        self.show_score("Hedgehog score", 810, 10, hedgehog_and_hamster_score)

        # print animals:
        self.window.blit(duck_img, (150, 375))
        self.window.blit(hedgehog_img, (750, 375))
        self.window.blit(dog_img, (150, 225))
        self.window.blit(hamster_img, (750, 225))

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
            self.duck_eats(1, eaten_apple_img)

        elif pygame.key.get_pressed()[pygame.K_a] and (
            self.poison.poison_x == 300 and self.poison.poison_y == 300
        ):
            self.duck_eats(-5, eaten_poison_img)

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
            self.hedgehog_eats(1, eaten_apple_img)

        elif pygame.key.get_pressed()[pygame.K_UP] and (
            self.poison.poison_x == 600 and self.poison.poison_y == 300
        ):
            self.hedgehog_eats(-5, eaten_poison_img)

    def show_text(self, text, font, x, y):
        text_on_screen = font.render(text, True, (255, 255, 255))
        self.window.blit(text_on_screen, (x, y))

    def draw_start_screen(self):
        self.window.fill((130, 30, 30))
        font = pygame.font.SysFont(None, 40)

        # show game title
        self.show_text("Hungry Hippos,", font, 400, 50)
        self.show_text("but hippos are duck, hedgehog, dog and hamster", font, 200, 100)

        # show first team
        self.show_text("Team I", font, 235, 275)
        self.window.blit(duck_screen_img, (225, 325))
        self.show_text("press D to catch food", font, 135, 485)

        # show second team
        self.show_text("Team II", font, 685, 275)
        self.window.blit(hedgehog_screen_img, (665, 325))
        self.show_text("press H to catch food", font, 600, 485)

        # pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        self.show_text("Press SPACE to start", font, 365, 625)
        pygame.display.update()
