import math

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


def plotPolarAll(data_frame):
    """
    Plots the polar diagram for a boat described by data frame and interpolates curves
    :param data_frame: polar diagram as data frame
    :return: List of interpolations for each wind speed described by data_frame
    """
    columns = data_frame.columns[1:]
    angles = list(map(math.radians, data_frame["Angle"]))
    angles_ext = np.arange(0, 2*math.pi, 0.01)

    # creating dictionary of interpolations
    interpolations = {}
    for cl in columns:
        itp = CubicSpline(angles, data_frame[cl])
        interpolations[cl] = itp

    # Evaluating interpolation for wider spectrum of angles
    ys_ext = {}
    for cl in columns:
        ys_ext[cl] = interpolations[cl](angles_ext)

    # Plotting results
    colors = [
        'blue',
        'orange',
        'green',
        'red',
        'purple',
        'brown',
        'pink',
        'gray'
    ]
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    color_idx = 0
    for cl in columns:
        ax.plot(angles, data_frame[cl], 'o', color=colors[color_idx])
        ax.plot(angles_ext, ys_ext[cl], color=colors[color_idx])
        color_idx += 1
    plt.show()

    # Returns dictionary with calculated interpolations
    return interpolations


def plotPolar(interpolation, x, y, x_ext):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(x, y, 'o', label='data')
    y_ext = interpolation(x_ext)
    ax.plot(x_ext, y_ext, label='itp')
    plt.show()
    return y_ext


if __name__ == '__main__':
    polar_df = pd.read_csv("SailboatData/polar_data_ext.csv")
    itps = plotPolarAll(polar_df)
    print(itps["Wind20"](math.radians(100)))
