import pygame

from apple import Apple
from poison import Poison
from game import Game


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    # create the game window 1050x750
    window = pygame.display.set_mode((1050, 750))

    # set font size to 36
    font = pygame.font.Font(None, 36)

    frame = pygame.Rect(0, 0, 0, 0)
    background_tile = pygame.Rect(0, 0, 0, 0)

    # possible arrangement of food in the frame
    food_pos_x = [300, 450, 600]
    food_pos_y = [150, 300, 450]

    apple_obj = Apple(food_pos_x, food_pos_y, window)
    poison_obj = Poison(food_pos_x, food_pos_y, window)
    game = Game(poison_obj, apple_obj, window)
    game.start(font, frame, background_tile)
