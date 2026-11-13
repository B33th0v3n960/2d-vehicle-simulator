from math import pi, sqrt
from random import randrange
from typing import Iterable, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist

from controller import Control 
from track import Track
from vehicle import Vehicle

dt = 0.05
v = 5
l = 1.6
ld = 3
duration = 30
car = Vehicle(1, 1, 0, v, l)
track = Track.s_track_gen(40, 20)



def main() -> None:
    matplotlib.use("QTAgg")
    plt.style.use("./mplstyles/nord-dark-talk.mplstyle")

    fig, axis = plt.subplots()
    (line,) = axis.plot([], [], lw=3)
    axis.set_xlim(-20, 20)
    axis.set_ylim(-5, 20)

    xpoints: list[float] = []
    ypoints: list[float] = []

    xtrack: list[float] = []
    ytrack: list[float] = []
    track_index = 0
    target = track[track_index]

    for point in track:
        xtrack.append(point[0])
        ytrack.append(point[1])

    def init() -> Iterable[Artist]:
        line.set_data([], [])
        return (line,)

    def animate(i) -> Iterable[Artist]:
        nonlocal track_index, target
        if Control.distance(car.x, car.y, target[0], target[1]) <= ld:
            track_index += 1
            track_index %= len(track)
            print(track_index)
        target = track[track_index]
        delta = Control.steer_car(car, ld, target)
        car.update(dt, delta)
        xpoints.append(car.x)
        ypoints.append(car.y)
        line.set_data(xpoints, ypoints)
        line.set_color("C3")
        return (line,)

    anim = FuncAnimation(
        fig, animate, init_func=init, frames=200, interval=20, blit=True
    )

    plt.plot(xtrack, ytrack, "o:", color="C1")
    # plt.axis("off")
    plt.axis("equal")
    plt.grid(visible=True)
    plt.show()


if __name__ == "__main__":
    main()
