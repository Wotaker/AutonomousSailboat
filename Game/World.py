from Utils import Wind, Buoy, generateText
from Boat import Boat

import random
import pygame
from pygame.sprite import Sprite

random.seed(420)


class World(Sprite):

    wind = Wind(45, 8)
    buoys = pygame.sprite.Group()
    buoys_dict = {}
    fleet = pygame.sprite.Group()
    background_color = (255, 255, 255)
    target_img = pygame.image.load("Images/target_trans_40x40.png")

    def __init__(self, screen, no_competitors, no_buoys=2):
        super().__init__()
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.no_buoys = no_buoys
        self.track_locations = (
            random.randint(0, self.width // 3),
            random.randint(2 * self.height // 3, self.height - 20),
            random.randint(2 * self.width // 3, self.width - 20),
            random.randint(0, self.height // 3),
        )

        # Adding Buoys to the lake
        self.buoys_dict[0] = Buoy(     # Starting Buoy
            self.track_locations[0],
            self.track_locations[1],
            buoy_type=0
        )
        self.buoys.add(self.buoys_dict[0])
        self.buoys_dict[no_buoys - 1] = Buoy(     # Finishing Buoy
            self.track_locations[2],
            self.track_locations[3],
            buoy_type=2
        )
        self.buoys.add(self.buoys_dict[no_buoys - 1])
        if no_buoys > 2:
            for i in range(1, no_buoys - 1):
                self.buoys_dict[i] = Buoy(
                    random.randint(0, self.width),
                    random.randint(0, self.height),
                    buoy_type=1
                )
                self.buoys.add(self.buoys_dict[i])

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
                0,
                False
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

    def startCountdown(self):
        for sec in range(3, 0, -1):
            self.screen.blit(*generateText(
                str(sec),
                'freesansbold.ttf',
                66,
                (self.width // 2, self.height // 2),
            ))
            pygame.display.update()
            pygame.time.wait(1000)
            self.screen.fill(self.background_color)
            self.draw(self.screen)

    def drawTarget(self, surface, target_position):
        rect = self.target_img.get_rect()
        rect.update(
            target_position[0] - rect.width / 2.,
            target_position[1] - rect.height / 2.,
            rect.width,
            rect.height)
        surface.blit(self.target_img, rect)

    def draw(self, surface):
        for boat in self.fleet:
            boat.draw(surface)
        self.wind.draw(surface)
        for buoy in self.buoys:
            buoy.draw(surface)
