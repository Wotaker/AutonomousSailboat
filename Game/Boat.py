import random

from Utils import blitRotateCenter
from Interpolations import crop2Dfunc

import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from scipy.optimize import minimize_scalar
import math
import cmath


class Boat(Sprite):

    pxl_size = 20           # Boat size in pixels
    velocity = 0            # boat speed (relative to water)
    velocity_moderator = 0.25     # speed multiplier constant
    rudder_step = 5
    dead_angle = 30
    surf = pygame.Surface((pxl_size, pxl_size))
    rect = surf.get_rect()

    def __init__(self, world, x_coord, y_coord, angle, speed_function,  player=False):
        super().__init__()
        self.world = world
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.angle = angle % 360
        self.speed_function = speed_function
        self.player = player
        self.target = None
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
                self.angle = (self.angle + self.rudder_step) % 360
                # print(f"BOAT (dir, speed) = ({self.angle}, {self.velocity})")
            elif pressed_keys[K_RIGHT]:
                self.angle = (self.angle - self.rudder_step) % 360
            elif self.target is not None:
                self.moveAutonomously()
        self.update_velocity()
        self.x_coord -= self.velocity * math.sin(math.radians(self.angle)) * self.velocity_moderator
        self.x_coord %= self.world.width
        self.y_coord -= self.velocity * math.cos(math.radians(self.angle)) * self.velocity_moderator
        self.y_coord %= self.world.height
        self.rect.update(self.x_coord, self.y_coord, self.pxl_size, self.pxl_size)

    def optimalCourse(self, target_coords):
        """
        Calculates the optimal course angle when heading to target
        :param target_coords: self explanatory
        :return: the optimal absolute angel
        """
        wind_speed = self.world.wind.speed
        w = self.world.wind.angle       # wind angle
        x_p, y_p = target_coords[0] - self.x_coord, target_coords[1] - self.y_coord
        b = (-math.degrees(cmath.polar(complex(x_p, y_p))[1]) - 90) % 360   # target angle
        a = b - w       # target angle relative to wind

        def velocityP(x):
            # Actually negative values, because we are maximizing speed with minimization
            if x > 30:
                return -(self.speed_function(x, wind_speed) * math.cos(math.radians(x - a)))
            else:
                return 0

        optimised = minimize_scalar(velocityP, bounds=(0, 360), method='Bounded')
        optimised_angle_relative = optimised.x              # optimal angle relative to wind
        # if random.random() > 0.95:
        #     print(f"Target: {target_coords}, Beta: {b}")
        return w + optimised_angle_relative                 # optimal absolute angle

    def moveAutonomously(self):
        optimal_course = self.optimalCourse(self.target)
        delta = ((180 - (self.angle - optimal_course)) % 360) - 180
        if delta > 0 and delta > self.rudder_step:
            delta = self.rudder_step
        elif delta < 0 and delta < -self.rudder_step:
            delta = -self.rudder_step
        else:
            delta = round(delta)
        if delta != 0:
            print(f"Rudder moved {delta} angles")
            self.angle = (self.angle + delta) % 360

    def update_velocity(self):
        """
        calculates and updates boats'  velocity
        :return: Nan
        """
        rel_abs_angle = abs(self.world.wind.angle - self.angle)
        if self.dead_angle < rel_abs_angle < 360 - self.dead_angle:
            self.velocity = self.speed_function(rel_abs_angle, self.world.wind.speed)
        else:
            self.velocity = 0

    def draw(self, surface):
        blitRotateCenter(surface, self.image, (self.x_coord, self.y_coord), self.angle)
