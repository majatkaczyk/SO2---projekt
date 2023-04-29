import pygame
import random
import threading
import time

from Apple import Apple
from Poison import Poison
from Game import Game


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((1050, 750))
    font = pygame.font.Font(None, 36)
    food_pos_x = [300, 450, 600]
    food_pos_y = [150, 300, 450]

    apple_obj = Apple(food_pos_x, food_pos_y, window)
    poison_obj = Poison(food_pos_x, food_pos_y, window)
    game = Game(poison_obj, apple_obj, window, font)
    game.start()
