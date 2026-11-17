from math import pi, sqrt
from random import randrange
from typing import Iterable

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.artist import Artist
from matplotlib.patches import Circle as Circle

from controller import Control
from track import Track
from vehicle import Vehicle


def main() -> None:
    dt = 0.05
    v = 5
    l = 1.6
    ld = 3
    car = Vehicle(0, 0, 0, v, l)
    track = Track.load_csv_track("./tracks/edgecase_waypoints.csv")
    track_loop = False
    lap_count = 0

    # matplotlib.use("QTAgg")
    # plt.style.use("./mplstyles/nord-dark-talk.mplstyle")
    fig, axis = plt.subplots()
    fig.tight_layout()
    (line,) = axis.plot([], [], lw=3)
    axis.set_aspect("equal", adjustable="datalim")
    look_ahead_circle = Circle((car.x, car.y), ld, fill=False)
    (car_point,) = axis.plot([car.x], [car.y], "o", color="C2")
    (draw_target_point,) = axis.plot([0], [0], "o", color="C6")
    axis.add_artist(look_ahead_circle)

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
        nonlocal track_index, target, lap_count, ld
        dist_to_next_waypoint = Control.distance((car.x, car.y), (target[0], target[1]))
        target_point = Control.get_target_point(
            (car.x, car.y),
            ld,
            track[(track_index - 1) % len(track)],
            track[track_index],
        )
        if dist_to_next_waypoint <= ld:
            track_index += 1
            if track_index == len(track) and dist_to_next_waypoint <= 0.5:
                lap_count += 1
                track_index = 0
            elif track_index == len(track):
                track_index = len(track) - 1

            ld = (
                Control.distance(track[(track_index - 1) % len(track)], track[track_index])
                / 8
            )
            ld = max(ld, 1)
            ld = min(ld, 3)

        target = track[track_index]
        delta = Control.steer_car(car, ld, target_point)
        if track_loop or lap_count == 0:
            view_height = 20
            bounding_box = axis.get_window_extent()
            aspect_ratio = bounding_box.width / bounding_box.height
            view_width = aspect_ratio * view_height
            car.update(dt, delta)
            axis.set_xlim(car.x - view_width, car.x + view_width)
            axis.set_ylim(car.y - view_height, car.y + view_height)

        xpoints.append(car.x)
        ypoints.append(car.y)
        line.set_data(xpoints, ypoints)

        look_ahead_circle.center = (car.x, car.y)
        look_ahead_circle.radius = ld
        car_point.set_data([car.x], [car.y])
        draw_target_point.set_data([target_point[0]], [target_point[1]])
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
