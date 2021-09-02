import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import math
import cmath
import scipy.optimize

from Interpolations import interpolateRbf, crop2Dfunc


if __name__ == '__main__':
    polar_df = pd.read_csv("SailboatData/polar_data_1.csv")
    print(math.cos(math.radians(-720 + 60)))
    print(math.degrees(cmath.polar(complex(-3, -2))[1]))

