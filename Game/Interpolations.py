import math
import numpy as np
import pandas as pd
import scipy as sp
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


def interpolateRbf(data_frame):
    """
    Interpolates a 2D surface to the data represented in data_frame
    :param data_frame: Data representing boats speed in relation to wind speed and attack angle
    :return: scipy.interpolate.Rbf object
    """
    wind_span = [6., 8., 10., 12., 14., 16., 20.]   # The measured wind speeds
    no_angles = np.shape(data_frame)[0]  # number of angles
    no_winds = len(wind_span)
    x = np.array(data_frame["Angle"]).repeat(no_winds)
    y = np.tile(np.array(wind_span), no_angles)
    fvals = data_frame.drop("Angle", axis=1)
    return sp.interpolate.Rbf(x, y, fvals, function='quintic', smooth=0.)


def testInterpolation(itp, wind_speed, test=True):
    """
    Tests the reliability of the interpolations, and plots the curve for specified wind speed
    :param itp: Tested interpolation
    :param wind_speed: Plotted wind speed
    :param test: If False, plots only, without additional tests
    :return: Nan
    """
    testRes = itp(polar_df["Angle"], [wind_speed] * np.shape(polar_df)[0])
    ang_idx = 0

    failed = []
    if test:
        for res in testRes:
            print(f"Angle {polar_df['Angle'][ang_idx]}: diff={round(polar_df['Wind8'][ang_idx] - res, 5)}, val={res}")
            if abs(round(polar_df['Wind8'][ang_idx] - res, 5)) > 10e-5:
                failed.append(polar_df['Angle'][ang_idx])
            ang_idx += 1
        if len(failed) != 0:
            print(f"TEST FAILED! Issues with angles {failed}")

    # Plots some results:
    xs = np.linspace(0, 360, 360)
    ys = itp(xs, [wind_speed] * 360)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(np.linspace(0, 2 * math.pi, 360), ys)
    ax.set_title("Polar plot for wind speed " + str(wind_speed))
    plt.show()


def plot2DInterpolation(itp2D, x_domain, y_domain, vrange=(0, 20), type='rbf'):
    """
    Plots interpolated function f(x, y) -> z
    :param itp2D: interpolated function
    :param x_domain: Xs Domain
    :param y_domain: Ys Domain
    :param vrange: (min, max) tuple representing minimal and maximal value of the plotted function
    :param type: type of the interpolation 'bisplrep' or 'rbf'
    :return:
    """
    y_ext, x_ext = np.meshgrid(y_domain, x_domain)
    z_ext = None
    if type == 'rbf':
        z_ext = itp2D(x_ext, y_ext)
    elif type == 'bisplrep':
        z_ext = sp.interpolate.bisplev(x_domain, y_domain, itp2D)
    else:
        print("Unknown interpolation type, please specify 'bisplrep' or 'rbf'")

    lims = dict(cmap='RdBu_r', vmin=vrange[0], vmax=vrange[1])
    plt.figure()
    plt.pcolormesh(x_ext, y_ext, z_ext, shading='auto', **lims)
    plt.colorbar()
    plt.title("Interpolated function.")
    plt.show()


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


def plotPolar(itp, x, y, x_ext):
    """
    Plots 1D interpolation of datapoints (x, y) on extended domain x_ext
    :param itp: interpolation
    :param x: x coordinates array of datapoints
    :param y: y coordinates array of datapoints
    :param x_ext: extended domain
    :return: interpolated array itp(x_ext)
    """
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(x, y, 'o', label='data')
    y_ext = itp(x_ext)
    ax.plot(x_ext, y_ext, label='itp')
    plt.show()
    return y_ext


def interpolate2D(data_frame, smooth=5):
    """
    Another interpolating function (beta version, not accurate results) use interpolateRbf() instead
    :param data_frame:
    :param smooth:
    :return:
    """
    ang_len = np.shape(data_frame)[0]  # number of angles
    wind_len = np.shape(data_frame)[1] - 1  # number of wind speeds
    ang = np.array([wind_len * [float(a)] for a in data_frame["Angle"]])
    wind = np.array([[6., 8., 10., 12., 14., 16., 20.] for a in range(ang_len)])
    z = data_frame.drop("Angle", axis=1)

    return sp.interpolate.bisplrep(ang, wind, z, s=smooth)


if __name__ == '__main__':
    polar_df = pd.read_csv("SailboatData/polar_data_ext.csv")

    # Rbf interpolation:
    rbfInt = interpolateRbf(polar_df)
    testInterpolation(rbfInt, 2, False)

    plot2DInterpolation(
        rbfInt,
        np.linspace(0., 360, 360),
        np.linspace(0., 20., 100),
        vrange=(0, 10),
        type='rbf'
    )




