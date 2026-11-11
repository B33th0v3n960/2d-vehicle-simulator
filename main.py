from math import pi
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, colormaps, colors
from numpy.typing import NDArray

from vehicle import Vehicle


def simulate() -> Tuple[NDArray[np.floating], NDArray[np.floating]]:
    dt = 0.05
    v = 5
    l = 1.6
    duration = 30
    delta = pi / 2
    car = Vehicle(1, 1, 0, v, l)
    xpoints = np.array([])
    ypoints = np.array([])

    test_time = 0
    while test_time < duration:
        car.update(dt, delta)
        test_time += dt
        # print(car)
        xpoints = np.append(xpoints, car.x)
        ypoints = np.append(ypoints, car.y)

    return xpoints, ypoints


def main() -> None:
    matplotlib.use("QTAgg")
    plt.style.use("./mplstyles/nord-dark-talk.mplstyle")

    xpoints, ypoints = simulate()
    plt.plot(xpoints, ypoints, "o:r")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
