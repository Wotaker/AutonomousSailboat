from Utils import Wind, Buoy
from Boat import Boat

import random
import pygame
from pygame.sprite import Sprite

random.seed(420)


class World(Sprite):

    wind = Wind(random.randint(0, 360), 5)
    buoys = []

    def __init__(self, width, height, no_buoys=4):
        super().__init__()
        self.width = width
        self.height = height
        self.track_locations = (
            random.randint(0, width // 3),
            random.randint(2 * height // 3, height),
            random.randint(2 * width // 3, width),
            random.randint(0, height // 3),
        )

        # Adding Players Boat
        self.myBoat = Boat(
            self,
            self.track_locations[0],
            self.track_locations[1] - 10,
            0
        )

        # Adding Buoys to the lake
        self.buoys.append(Buoy(     # Starting Buoy
            self.track_locations[0],
            self.track_locations[1],
            buoy_type=1
        ))
        self.buoys.append(Buoy(     # Finishing Buoy
            self.track_locations[2],
            self.track_locations[3],
            buoy_type=2
        ))
        if no_buoys > 2:
            for i in range(no_buoys - 2):
                self.buoys.append(Buoy(
                    random.randint(0, width),
                    random.randint(0, height),
                    buoy_type=0
                ))

    # TODO Moves all boats to the starting line
    def reset_positions(self):
        pass

    def changeWind(self, direction, speed):
        self.wind.angle = direction
        self.wind.speed = speed

    def draw(self, surface):
        self.myBoat.draw(surface)
        self.wind.draw(surface)
        for buoy in self.buoys:
            buoy.draw(surface)
