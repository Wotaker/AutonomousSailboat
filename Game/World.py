from Utils import Wind, Buoy
from Boat import Boat
from Interpolations import interpolateRbf

import random
import pygame
from pygame.sprite import Sprite
import pandas as pd

random.seed(420)


class World(Sprite):

    wind = Wind(0, 6)
    buoys = pygame.sprite.Group()
    fleet = pygame.sprite.Group()

    def __init__(self, width, height, no_competitors, no_buoys=2):
        super().__init__()
        self.width = width
        self.height = height
        self.track_locations = (
            random.randint(0, width // 3),
            random.randint(2 * height // 3, height - 20),
            random.randint(2 * width // 3, width - 20),
            random.randint(0, height // 3),
        )

        # Adding Boats
        self.player_boat = Boat(
            self,
            self.track_locations[0],
            self.track_locations[1] + 10,
            0,
            True
        )
        self.fleet.add(self.player_boat)
        for comp in range(no_competitors):
            self.fleet.add(Boat(
                self,
                self.track_locations[0] + 20,
                self.track_locations[1] + 10,
                30,
                False
            ))

        # Adding Buoys to the lake
        self.buoys.add(Buoy(     # Starting Buoy
            self.track_locations[0],
            self.track_locations[1],
            buoy_type=1
        ))
        self.buoys.add(Buoy(     # Finishing Buoy
            self.track_locations[2],
            self.track_locations[3],
            buoy_type=2
        ))
        if no_buoys > 2:
            for i in range(no_buoys - 2):
                self.buoys.add(Buoy(
                    random.randint(0, width),
                    random.randint(0, height),
                    buoy_type=0
                ))

    # TODO Moves all boats to the starting line
    def reset_positions(self):
        pass

    def moveBoats(self):
        for boat in self.fleet:
            boat.move()

    def changeWind(self, direction, speed):
        self.wind.angle = direction
        self.wind.speed = speed

    def draw(self, surface):
        for boat in self.fleet:
            boat.draw(surface)
        self.wind.draw(surface)
        for buoy in self.buoys:
            buoy.draw(surface)
