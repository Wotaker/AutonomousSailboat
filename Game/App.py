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

# Colors and fonts dictionaries
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 200, 0)
}

# Setup a display
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(colors.get("white"))
pygame.display.set_caption("Niegocin")


def gameLoop():
    # Creates new World Environment
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        # Reacts to occurring events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Redraws Display
        DISPLAYSURF.fill(colors.get("white"))

        # Move players boat
        world.myBoat.move()

        # Moves the rest of the boats

        # Updates display graphics
        world.draw(DISPLAYSURF)
        pygame.display.update()
        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    gameLoop()
