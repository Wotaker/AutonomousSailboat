from World import World
from Utils import generateText

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
    "green": (0, 200, 0),
    "gray": (115, 115, 115)
}


# Setup a display
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(colors.get("white"))
pygame.display.set_caption("Niegocin")


def gameLoop():

    running = True

    # Creates new World Environment
    world = World(DISPLAYSURF, 1, 10)
    world.draw(DISPLAYSURF)
    pygame.display.update()
    world.startCountdown()

    while True:
        # Reacts to occurring events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = not running
                elif event.key == pygame.K_v:
                    world.player_boat.optimalCourse(plot=True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                world.player_boat.target = pygame.mouse.get_pos()
                # print(f"Heading to: {world.player_boat.target}")

        if running:
            # Update state of the world
            world.wind.manuallyChange()
            world.moveBoats()

            # Updates display graphics
            DISPLAYSURF.fill(colors.get("white"))
            world.draw(DISPLAYSURF)
            pygame.display.update()

        else:
            DISPLAYSURF.blit(*generateText(
                'Press P to Start or Pause',
                'freesansbold.ttf',
                32,
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            ))
            pygame.display.update()

        FramePerSecond.tick(FPS)


if __name__ == '__main__':
    gameLoop()
