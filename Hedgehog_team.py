import pygame

eaten_apple_img = pygame.image.load("assets/eaten_apple.png")
eaten_poison_img = pygame.image.load("assets/eaten_poison.png")

haps_yellow = pygame.image.load("assets/haps_yellow.png")


class Hedgehog_team:
    def __init__(self, semaphore, lock, window):
        self.hedgehog_and_hamster_score = 0
        self.semaphore = semaphore
        self.lock = lock
        self.window = window

    def logic(self, apple, poison):
        # if food appears at x = 600 and y = 300, the hedgehog team can catch it

        if (
            pygame.key.get_pressed()[pygame.K_h]
            and (apple.apple_x == 600 and apple.apple_y == 300)
            and (poison.poison_x == 600 and poison.poison_y == 300)
        ):
            # if apple and poison are in the same spot and the H key was pressed, nothing happens
            pygame.time.wait(650)

        elif pygame.key.get_pressed()[pygame.K_h] and (
            apple.apple_x == 600 and apple.apple_y == 300
        ):
            # if the H key was pressed and the apple is in the right place,the hedgehog team eats apple and get +1 point
            self.eat(1, eaten_apple_img, self.semaphore, self.lock)

        elif pygame.key.get_pressed()[pygame.K_h] and (
            poison.poison_x == 600 and poison.poison_y == 300
        ):
            # if the H key was pressed and the poison is in the right place,the hedgehog team eats poison and get -5 points
            self.eat(-5, eaten_poison_img, self.semaphore, self.lock)

    def eat(self, score, img, semaphore, lock):
        # new threads can only acquire a position on the semaphore once an existing thread holding the semaphore releases a position
        semaphore.acquire()
        lock.acquire()

        # update score
        self.hedgehog_and_hamster_score += score

        # update game window
        pygame.display.update()

        # show eaten food on screen
        self.draw_eaten_food(img, 600, 300)

        # show "haps" above the team for 1.5 s
        self.window.blit(haps_yellow, (750, 100))
        pygame.time.wait(1500)

        # release the position
        lock.release()
        semaphore.release()

    def draw_eaten_food(self, img, x_pos, y_pos):
        # hide whole food
        shape = pygame.rect.Rect(x_pos, y_pos, 150, 150)
        pygame.draw.rect(self.window, (130, 30, 30), shape)
        # show eaten food
        self.window.blit(img, (x_pos, y_pos))
