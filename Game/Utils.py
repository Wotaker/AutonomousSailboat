import cv2
import pygame
from pygame import transform
from pygame.sprite import Sprite
from pygame.locals import *


class Buoy(Sprite):

    pxl_size = 20
    surf = pygame.Surface((pxl_size, pxl_size))

    def __init__(self, x_coord, y_coord, buoy_type=0):
        super(Buoy, self).__init__()
        self.type = buoy_type   # 0, 1, 2 means as follows: regular, start, finish
        if buoy_type == 0:
            self.image = pygame.image.load("Images/buoy_reg_trans.png")
        elif buoy_type == 1:
            self.image = pygame.image.load("Images/buoy_go.png")
        else:
            self.image = pygame.image.load("Images/buoy_finish.png")
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.rect = self.surf.get_rect()
        self.rect.update(self.x_coord, self.y_coord, self.pxl_size, self.pxl_size)
        self.print()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def print(self):
        print(f"New Buoy of type {self.type} at location {(self.x_coord, self.y_coord)}")


class Wind:

    pxl_size = 50       # Size of wind arrow in pixels
    image = pygame.image.load("Images/arrow_trans.png")
    surf = pygame.Surface((pxl_size, pxl_size))

    def __init__(self, angle, speed):
        self.angle = angle % 360    # wind angle in degrees
        self.speed = speed
        self.rect = self.surf.get_rect()

    def manuallyChange(self):
        """
        Controls wind with W, A, S, D keys
        :return: Nan
        """
        unit = 1
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            self.angle = (self.angle + 5) % 360
            # print(f"WIND (dir, speed) = ({self.angle}, {self.speed})")
        elif pressed_keys[K_d]:
            self.angle = (self.angle - 5) % 360
        if pressed_keys[K_w]:
            self.speed += unit
        elif pressed_keys[K_s] and self.speed >= unit:
            self.speed -= unit

    def draw(self, surface):
        blitRotateCenter(surface, self.image, (10, 10), self.angle)


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotates an image, and draws it on to the surface
    :param surf: The surface to be drawn on
    :param image: The image which will be drawn on the surface surf
    :param topleft: the top left coordinates of the image
    :param angle: The angle of rotation
    :return: Rotated image and bounding rectangle
    """
    rotated_image = transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)
    return rotated_image, new_rect


def resizeImage(source, dest, new_size):
    """
    Resizes an image and saves it
    :param source: The source image path
    :param dest: The path to the new image
    :param new_size: The tuple (width, height) describing the new image shape
    :return: Nan
    """
    img = cv2.imread(source)
    img = cv2.resize(img, new_size)
    cv2.imwrite(dest, img)


if __name__ == '__main__':
    resizeImage("Images/buoy_raw.png", "Images/buoy_30x30.png", (30, 30))

