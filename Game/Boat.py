import random

from Utils import blitRotateCenter
from Interpolations import plotFunc, interpolateRbf

import numpy as np
import pandas as pd
import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from scipy.optimize import minimize_scalar
import math
import cmath


def sgn(x):
    return 2 * (x > 0) - 1


class Boat(Sprite):

    pxl_size = 20           # Boat size in pixels
    speedFunction = interpolateRbf(pd.read_csv("SailboatData/polar_data_1.csv"))
    velocity = 0            # boat speed (relative to water)
    velocity_moderator = 0.25     # speed multiplier constant
    rudder_step = 5
    dead_angle = 30
    tack_angle = 15
    surf = pygame.Surface((pxl_size, pxl_size))
    rect = surf.get_rect()

    def __init__(self, world, x_coord, y_coord, angle,  player=False):
        super().__init__()
        self.world = world
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.angle = angle % 360
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

    @staticmethod
    def angle_diff(minuend, subtrahend):
        return ((180 - (subtrahend - minuend)) % 360) - 180

    def optimalCourse(self, plot=False):
        """
        Calculates the optimal course angle when heading to target
        :param plot: To plot the velocity_P(angle)
        :return: the optimal absolute angel
        """
        wind_speed = self.world.wind.speed
        w = self.world.wind.angle       # wind angle
        x_p, y_p = self.target[0] - self.x_coord, self.target[1] - self.y_coord
        b = (-math.degrees(cmath.polar(complex(x_p, y_p))[1]) - 90) % 360   # target angle
        a = self.angle_diff(b, w) % 360

        def velocity_P(x):
            # Actually negative values, because we are maximizing speed with minimization
            if 30 < x < 330:
                return -(self.speedFunction(x, wind_speed) * math.cos(math.radians(x - a)))
            else:
                return 0

        if random.random() > 0.95:
            print(f"Target: {self.target}, Beta: {b}, Alfa: {a}")

        if plot:
            plotFunc(velocity_P, np.linspace(0, 360, 360), f"Velocity in P direction, wind={wind_speed}")

        # if a < self.tack_angle or a > 360 - self.tack_angle:
        #     return self.angle
        # else:
        #     optimised = minimize_scalar(velocity_P, bounds=(0, 360), method='Bounded')
        #     optimised_angle_relative = optimised.x              # optimal angle relative to wind
        #     return w + optimised_angle_relative                 # optimal absolute angle

        # optimised = minimize_scalar(velocity_P, bounds=(0, 360), method='Bounded')
        # optimised_angle_relative = optimised.x  # optimal angle relative to wind
        # return w + optimised_angle_relative  # optimal absolute angle

        if a < self.tack_angle or a > 360 - self.tack_angle:
            if self.angle_diff(self.angle, w) < 0:
                optimised = minimize_scalar(velocity_P, bounds=(270, 360), method='Bounded')
                optimised_angle_relative = optimised.x              # optimal angle relative to wind
            else:
                optimised = minimize_scalar(velocity_P, bounds=(0, 90), method='Bounded')
                optimised_angle_relative = optimised.x
        else:
            optimised = minimize_scalar(velocity_P, bounds=(0, 360), method='Bounded')
            optimised_angle_relative = optimised.x              # optimal angle relative to wind
        return w + optimised_angle_relative  # optimal absolute angle

    def moveAutonomously(self):
        optimal_course = self.optimalCourse()
        delta = self.angle_diff(optimal_course, self.angle)
        if delta > 0 and delta > self.rudder_step:
            delta = self.rudder_step
        elif delta < 0 and delta < -self.rudder_step:
            delta = -self.rudder_step
        else:
            delta = round(delta)
        if delta != 0:
            # print(f"Rudder moved {delta} angles")
            self.angle = (self.angle + delta) % 360

    def update_velocity(self):
        """
        calculates and updates boats'  velocity
        :return: Nan
        """
        rel_abs_angle = abs(self.world.wind.angle - self.angle)
        if self.dead_angle < rel_abs_angle < 360 - self.dead_angle:
            self.velocity = self.speedFunction(rel_abs_angle, self.world.wind.speed)
        else:
            self.velocity = 0

    def draw(self, surface):
        blitRotateCenter(surface, self.image, (self.x_coord, self.y_coord), self.angle)
