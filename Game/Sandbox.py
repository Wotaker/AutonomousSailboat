import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import math
import cmath

import pygame.font
import scipy.optimize
from scipy.stats import norm

from Interpolations import plotFunc


def sgn(x):
    return 2 * (x > 0) - 1


def angle_diff(minuend, subtrahend):
    return ((180 - (subtrahend - minuend)) % 360) - 180


if __name__ == '__main__':
    print(pygame.font.get_fonts())

