import pygame
import random
import time

apple_img = pygame.image.load("assets/apple.png")


class Apple:
    def __init__(self, food_pos_x, food_pos_y, window):
        self.apple_x = random.choice(food_pos_x)
        self.apple_y = random.choice(food_pos_y)

        # arrays of possible apple arrangements on the board
        self.food_pos_x = food_pos_x
        self.food_pos_y = food_pos_y

        # game window
        self.window = window

    def apple(self):
        # random apple spot
        self.apple_x = random.choice(self.food_pos_x)
        self.apple_y = random.choice(self.food_pos_y)

        time.sleep(0.30)

        # show apple on game window
        self.window.blit(apple_img, (self.apple_x, self.apple_y))

    def change_position(self):
        self.apple_x = random.choice(self.food_pos_x)
        self.apple_y = random.choice(self.food_pos_y)
