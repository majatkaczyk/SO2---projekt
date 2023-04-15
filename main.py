import pygame
import random
import threading
import time

pygame.init()
pygame.font.init()
window = pygame.display.set_mode((1050, 750))
font = pygame.font.Font(None, 36)

duckImg = pygame.image.load("assets/kaczuszka.png")
hedgehogImg = pygame.image.load("assets/hedgehog.png")
appleImg = pygame.image.load("assets/apple.png")
haps_yellow = pygame.image.load("assets/haps_yellow.png")
poisonImg = pygame.image.load("assets/poison.png")
eatenAppleImg = pygame.image.load("assets/eaten_apple.png")

food_pos_x = [300, 450, 600]
food_pos_y = [150, 300, 450]

score = 0


class Apple:
    def __init__(self, apple_x, apple_y):
        self.apple_x = apple_x
        self.apple_y = apple_y

    def apple(self):
        self.apple_x = random.choice(food_pos_x)
        self.apple_y = random.choice(food_pos_y)
        time.sleep(0.10)
        window.blit(appleImg, (self.apple_x, self.apple_y))


class Poison:
    def __init__(self, poison_x, poison_y):
        self.poison_x = random.choice(food_pos_x)
        self.poison_y = random.choice(food_pos_y)

    def poison(self):
        self.poison_x = random.choice(food_pos_x)
        self.poison_y = random.choice(food_pos_y)
        # pygame.time.delay(140)
        # time.sleep(0.15)
        time.sleep(0.15)
        window.blit(poisonImg, (self.poison_x, self.poison_y))


class Game:
    def __init__(self, poison: Poison, apple: Apple):
        self.frame = pygame.rect.Rect(298, 148, 454, 454)
        self.background_tile = pygame.rect.Rect(300, 150, 450, 450)
        self.poison = poison
        self.apple = apple

    def start(self):
        global score
        run = True

        while run:
            for event in pygame.event.get():
                # close the window:
                if event.type == pygame.QUIT:
                    run = False

            # add background color:
            window.fill((130, 30, 30))
            pygame.draw.rect(window, (255, 255, 255), self.frame)
            pygame.draw.rect(window, (130, 30, 30), self.background_tile)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            window.blit(score_text, (10, 10))

            # print duck:
            window.blit(duckImg, (150, 300))
            window.blit(hedgehogImg, (750, 300))
            appleThread = threading.Thread(target=self.apple.apple)
            poisonThread = threading.Thread(target=self.poison.poison)
            appleThread.start()
            poisonThread.start()
            appleThread.join()
            poisonThread.join()

            if pygame.key.get_pressed()[pygame.K_SPACE] and (
                apple.apple_x == 300 and apple.apple_y == 300
            ):
                self.duckEats()
            if pygame.key.get_pressed()[pygame.K_SPACE] and (
                poison.poison_x == 300 and poison.poison_y == 300
            ):
                score = 0
                self.draw_game_over_screen()
                run = False
                pygame.time.wait(2000)
            pygame.display.update()

    def duckEats(self):
        global score
        score += 1
        pygame.display.update()
        apple.apple_x = 300
        apple.apple_y = 300
        window.blit(appleImg, (300, 300))
        shape = pygame.rect.Rect(300, 300, 150, 150)
        pygame.draw.rect(window, (130, 30, 30), shape)
        window.blit(eatenAppleImg, (300, 300))
        # time.sleep(2)
        window.blit(haps_yellow, (150, 150))
        pygame.time.wait(650)

    def draw_game_over_screen(self):
        pygame.display.update()
        pygame.time.wait(650)
        window.fill((130, 30, 30))
        font = pygame.font.SysFont(None, 40)
        title = font.render("Game Over, you ate poison :(", True, (255, 255, 255))
        pygame.draw.rect(window, (130, 30, 30), self.background_tile)
        window.blit(
            title, (1050 / 2 - title.get_width() / 2, 750 / 2 - title.get_height() / 3)
        )
        pygame.display.update()


if __name__ == "__main__":
    apple_x = random.choice(food_pos_x)
    apple_y = random.choice(food_pos_y)
    poison_x = random.choice(food_pos_x)
    poison_y = random.choice(food_pos_y)
    apple = Apple(apple_x, apple_y)
    poison = Poison(poison_x, poison_y)
    game = Game(poison, apple)
    game.start()
