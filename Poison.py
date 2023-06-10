import pygame
import random
import time

poison_img = pygame.image.load("assets/poison.png")


class Poison:
    def __init__(self, food_pos_x, food_pos_y, window):
        self.poison_x = random.choice(food_pos_x)
        self.poison_y = random.choice(food_pos_y)

        # arrays of possible poison arrangements on the board
        self.food_pos_x = food_pos_x
        self.food_pos_y = food_pos_y

        # game window
        self.window = window

    def poison(self):
        # random poison spot
        self.poison_x = random.choice(self.food_pos_x)
        self.poison_y = random.choice(self.food_pos_y)

        time.sleep(0.30)

        # show apple on game window
        self.window.blit(poison_img, (self.poison_x, self.poison_y))

    def change_position(self):
        self.poison_x = random.choice(self.food_pos_x)
        self.poison_y = random.choice(self.food_pos_y)
