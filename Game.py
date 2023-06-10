import pygame
import random
import threading
import time

from Apple import Apple
from Poison import Poison
from Duck_team import Duck_team
from Hedgehog_team import Hedgehog_team

# load pet images
duck_img = pygame.image.load("assets/duck.png")
hedgehog_img = pygame.image.load("assets/hedgehog.png")
dog_img = pygame.image.load("assets/dog.png")
hamster_img = pygame.image.load("assets/hamster.png")

# load pets images for start and game over screen
duck_screen_img = pygame.image.load("assets/duck_win.png")
hedgehog_screen_img = pygame.image.load("assets/hedgehog_win.png")


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

        # add lock
        self.lock = threading.Lock()

        # create teams
        self.duck_team = Duck_team(self.lock, self.window)
        self.hedgehog_team = Hedgehog_team(self.lock, self.window)

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

            # if space pressed hide start screen and draw game board
            if self.game_state == "game_started":
                self.frame = pygame.rect.Rect(298, 148, 454, 454)
                self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
                self.draw_game()

                # add threads
                apple_thread = threading.Thread(target=self.apple.apple)
                poison_thread = threading.Thread(target=self.poison.poison)
                apple_thread.start()
                poison_thread.start()
                apple_thread.join()
                poison_thread.join()

                self.duck_team.logic(self.apple, self.poison)

                # if the duck team has less than 0 points, then hedgehog team wins and show game over screen for 3 s
                if self.duck_team.duck_and_dog_score < 0:
                    self.draw_game_over_screen("Hedgehog team wins!", 390, 175)
                    run = False
                    pygame.time.wait(3000)

                self.hedgehog_team.logic(self.apple, self.poison)

                # if the hedgehog team has less than 0 points, then duck team wins and show game over screen for 3 s
                if self.hedgehog_team.hedgehog_and_hamster_score < 0:
                    self.draw_game_over_screen("Duck team wins!", 420, 175)
                    run = False
                    pygame.time.wait(3000)

                pygame.display.update()

    def draw_game_over_screen(self, text, pos_x, pos_y):
        # update game window
        pygame.display.update()
        pygame.time.wait(1000)

        # fill game window window with a maroon color
        self.window.fill((130, 30, 30))

        # set font size to 40
        font = pygame.font.SysFont(None, 40)
        self.show_text("GAME OVER", font, 450, 100)

        # show which team won the game
        self.show_text(text, font, pos_x, pos_y)

        self.show_text("Duck team", font, 200, 275)
        self.window.blit(duck_screen_img, (200, 315))

        self.show_text("Hedgehog team", font, 670, 275)
        self.window.blit(hedgehog_screen_img, (700, 315))

        # show the duck team score
        self.show_score("Score", 210, 480, self.duck_team.duck_and_dog_score)

        # show the hedgehog team score
        self.show_score(
            "Score", 715, 480, self.hedgehog_team.hedgehog_and_hamster_score
        )

        pygame.display.update()

    def show_score(self, text, x_pos, y_pos, score):
        score_text = self.font.render(f"{text}: {score}", True, (255, 255, 255))
        self.window.blit(score_text, (x_pos, y_pos))

    def draw_game(self):
        # add background color
        self.window.fill((130, 30, 30))

        # show white frame and maroon background
        pygame.draw.rect(self.window, (255, 255, 255), self.frame)
        pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)

        # print score
        self.show_score("Duck team score", 20, 10, self.duck_team.duck_and_dog_score)
        self.show_score(
            "Hedgehog team score",
            720,
            10,
            self.hedgehog_team.hedgehog_and_hamster_score,
        )

        # print animals images
        self.window.blit(duck_img, (150, 375))
        self.window.blit(hedgehog_img, (750, 375))
        self.window.blit(dog_img, (150, 225))
        self.window.blit(hamster_img, (750, 225))

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
        self.show_text("Duck team", font, 235, 275)
        self.window.blit(duck_screen_img, (225, 325))
        self.show_text("press D to catch food", font, 165, 485)

        # show second team
        self.show_text("Hedgehog team", font, 625, 275)
        self.window.blit(hedgehog_screen_img, (665, 325))
        self.show_text("press H to catch food", font, 600, 485)

        # pygame.draw.rect(self.window, (130, 30, 30), self.background_tile)
        self.show_text("Press SPACE to start", font, 365, 625)
        pygame.display.update()
