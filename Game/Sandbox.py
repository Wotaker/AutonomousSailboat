import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


def tutorialTest():
    x_edges, y_edges = np.mgrid[-1:1:21j, -1:1:21j]
    print(x_edges[:2, 0])
    x = x_edges[:-1, :-1] + np.diff(x_edges[:2, 0])[0] / 2.
    y = y_edges[:-1, :-1] + np.diff(y_edges[0, :2])[0] / 2.
    z = (x + y) * np.exp(-6.0 * (x * x + y * y))
    print(x)
    print(y)

    plt.figure()
    lims = dict(cmap='RdBu_r', vmin=-0.25, vmax=0.25)
    plt.pcolormesh(x_edges, y_edges, z, shading='flat', **lims)
    plt.colorbar()
    plt.title("Sparsely sampled function.")
    plt.show()

    xnew_edges, ynew_edges = np.mgrid[-1:1:71j, -1:1:71j]
    xnew = xnew_edges[:-1, :-1] + np.diff(xnew_edges[:2, 0])[0] / 2.
    ynew = ynew_edges[:-1, :-1] + np.diff(ynew_edges[0, :2])[0] / 2.
    tck = interpolate.bisplrep(x, y, z, s=0)
    # print(interpolate.bisplev(np.array([-0.232]), np.array([-0.54]), tck))
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    plt.figure()
    plt.pcolormesh(xnew_edges, ynew_edges, znew, shading='flat', **lims)
    plt.colorbar()
    plt.title("Interpolated function.")
    plt.show()


if __name__ == '__main__':
    tutorialTest()
