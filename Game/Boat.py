from Utils import blitRotateCenter

import pygame
from pygame.locals import *
from pygame.sprite import Sprite
import math


class Boat(Sprite):

    pxl_size = 20           # Boat size in pixels
    velocity = 0            # boat speed (relative to water)
    velocity_factor = 2     # speed multiplier constant
    surf = pygame.Surface((pxl_size, pxl_size))
    rect = surf.get_rect()

    def __init__(self, world, x_coord, y_coord, angle, player=False):
        super().__init__()
        self.world = world
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.angle = angle
        self.player = player
        if player:
            self.image = pygame.image.load("Images/sailboat_trans_blue.png")
        else:
            self.image = pygame.image.load("Images/sailboat_green.png")
        self.rect.update(self.x_coord, self.y_coord, self.pxl_size, self.pxl_size)

    def move(self):
        """
        moves the boat in reaction to keyboard events (left and right keys) if player, or autonomously otherwise
        :return: Nan
        """
        if self.player:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                self.angle = (self.angle + 5) % 360
            elif pressed_keys[K_RIGHT]:
                self.angle = (self.angle - 5) % 360
        else:
            self.moveAutonomously()
        self.update_velocity(self.world.wind.angle)
        self.x_coord -= self.velocity * math.sin(math.radians(self.angle))
        self.x_coord %= self.world.width
        self.y_coord -= self.velocity * math.cos(math.radians(self.angle))
        self.y_coord %= self.world.height
        self.rect.update(self.x_coord, self.y_coord, self.pxl_size, self.pxl_size)

    def moveAutonomously(self):
        pass

    def update_velocity(self, wind_angle):
        """
        calculates and updates boats'  velocity
        :param wind_angle: the absolute wind angle (relative to the north)
        :return: Nan
        """
        rel_abs_angle = abs(wind_angle - self.angle)

        # TODO Replace below line with function calculating speed from polar chart
        self.velocity = self.world.wind.speed * (math.cos(math.radians(rel_abs_angle) / 2) ** 2)
        # print(f"Relative Angle: {rel_abs_angle}, Speed: {self.velocity}")

    def draw(self, surface):
        blitRotateCenter(surface, self.image, (self.x_coord, self.y_coord), self.angle)
