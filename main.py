from math import pi, sqrt
from random import randrange
from typing import Iterable

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist

from controller import Control
from track import Track
from vehicle import Vehicle


def main() -> None:
    dt = 0.05
    v = 5
    l = 1.6
    ld = 3
    car = Vehicle(1, 1, 0, v, l)
    track = Track.load_csv_track("./tracks/edgecase_waypoints.csv")
    track_loop = False
    lap_count = 0

    # matplotlib.use("QTAgg")
    # plt.style.use("./mplstyles/nord-dark-talk.mplstyle")
    fig, axis = plt.subplots()
    fig.tight_layout()
    (line,) = axis.plot([], [], lw=3)
    axis.set_aspect("equal", adjustable="datalim")

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
        nonlocal track_index, target, lap_count
        if Control.distance(car.x, car.y, target[0], target[1]) <= ld:
            track_index += 1
            if track_index == len(track):
                lap_count += 1
                track_index = 0
            # print(track_index)
        target = track[track_index]
        delta = Control.steer_car(car, ld, target)
        if track_loop or lap_count == 0:
            car.update(dt, delta)
        xpoints.append(car.x)
        ypoints.append(car.y)
        line.set_data(xpoints, ypoints)

        view_height = 20
        bounding_box = axis.get_window_extent()
        aspect_ratio = bounding_box.width / bounding_box.height
        view_width = aspect_ratio * view_height
        axis.set_xlim(car.x - view_width, car.x + view_width)
        axis.set_ylim(car.y - view_height, car.y + view_height)
        line.set_color("C3")
        return (line,)

    anim = FuncAnimation(
        fig, animate, init_func=init, frames=200, interval=20, blit=False
    )

    plt.plot(xtrack, ytrack, "o:", color="C1")
    # plt.axis("off")
    plt.grid(visible=True)
    plt.show()


if __name__ == "__main__":
    main()
