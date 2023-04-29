import pygame
import random
import time

poison_img = pygame.image.load("assets/poison.png")


class Poison:
    def __init__(self, food_pos_x, food_pos_y, window):
        self.poison_x = random.choice(food_pos_x)
        self.poison_y = random.choice(food_pos_y)
        self.food_pos_x = food_pos_x
        self.food_pos_y = food_pos_y
        self.window = window

    def poison(self):
        self.poison_x = random.choice(self.food_pos_x)
        self.poison_y = random.choice(self.food_pos_y)
        # pygame.time.delay(140)
        # time.sleep(0.15)
        time.sleep(0.30)
        self.window.blit(poison_img, (self.poison_x, self.poison_y))
