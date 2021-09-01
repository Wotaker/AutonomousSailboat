from World import World

import pygame
import sys
import random
from pygame.locals import *


# Initialize program
random.seed(420)
pygame.init()

# Controls the refresh speed
FPS = 30
FramePerSecond = pygame.time.Clock()

# Colors and fonts
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 200, 0)
}
font = pygame.font.Font('freesansbold.ttf', 32)
# pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))


# Setup a display
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(colors.get("white"))
pygame.display.set_caption("Niegocin")

# Setup pause screen
pause_text = font.render('Press P to Start or Pause', True, colors["black"], colors["white"])
pause_rect = pause_text.get_rect()
pause_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def gameLoop():

    running = True
    first_run = True

    # Creates new World Environment
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT, 1)

    while True:
        # Reacts to occurring events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = not running

        if running:
            # Update state of the world
            world.wind.manuallyChange()
            world.moveBoats()

            # Updates display graphics
            DISPLAYSURF.fill(colors.get("white"))
            world.draw(DISPLAYSURF)
            pygame.display.update()
            if first_run:
                running = False
                first_run = False
        else:
            DISPLAYSURF.blit(pause_text, pause_rect)
            pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    gameLoop()
