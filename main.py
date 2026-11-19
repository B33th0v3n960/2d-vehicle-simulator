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
    track = Track.load_csv_track("./tracks/silverstone_waypoints.csv")
    track_loop = False
    lap_count = 0
    xpoints: list[float] = []
    ypoints: list[float] = []
    xtrack: list[float] = []
    ytrack: list[float] = []
    track_index = 0
    waypoint = track[track_index]

    # matplotlib.use("QTAgg")
    # plt.style.use("./mplstyles/nord-dark-talk.mplstyle")
    fig, axis = plt.subplots()
    fig.tight_layout()
    (line,) = axis.plot([], [], lw=3)
    line.set_color("C3")
    axis.set_aspect("equal", adjustable="datalim")
    look_ahead_circle = Circle((car.x, car.y), ld, fill=False)
    (car_point,) = axis.plot([car.x], [car.y], "o", color="C2")
    (draw_target_point,) = axis.plot([0], [0], "o", color="C6")
    axis.add_artist(look_ahead_circle)
    plt.grid(visible=True)

    for point in track:
        xtrack.append(point[0])
        ytrack.append(point[1])
    plt.plot(xtrack, ytrack, "o:", color="C1")

    def init() -> Iterable[Artist]:
        line.set_data([], [])
        return (line,)

    def animate(i) -> Iterable[Artist]:
        nonlocal track_index, waypoint, lap_count, ld
        pos = (car.x, car.y)
        for _ in range(len(track)):
            if Control.distance(pos, track[track_index]) > ld:
                break
            if track_loop:
                if track_index == 0:
                    lap_count += 1
                track_index = (track_index + 1) % len(track)
            else:
                if track_index == len(track) - 1:
                    break
                track_index += 1
        waypoint = track[track_index]

        if (
            not track_loop
            and lap_count == 0
            and track_index == len(track) - 1
            and Control.distance(pos, track[-1]) <= 0.5
        ):
            lap_count = 1

        target_point = Control.get_target_point(
            pos,
            ld,
            track[(track_index - 1) % len(track)],
            track[track_index],
        )
        delta = Control.steer_car(car, ld, target_point)

        if track_loop or lap_count == 0:
            v_target = Control.target_speed(car, ld, target_point)
            k = 0.4
            ld = min(max(k * car.velocity, 1.0), 10.0)
            car.accelerate(v_target, dt)
            car.update(dt, delta)

            view_height = 50
            bounding_box = axis.get_window_extent()
            aspect_ratio = bounding_box.width / bounding_box.height
            view_width = aspect_ratio * view_height
            axis.set_xlim(car.x - view_width, car.x + view_width)
            axis.set_ylim(car.y - view_height, car.y + view_height)

        xpoints.append(car.x)
        ypoints.append(car.y)
        line.set_data(xpoints, ypoints)
        look_ahead_circle.center = (car.x, car.y)
        look_ahead_circle.radius = ld
        car_point.set_data([car.x], [car.y])
        draw_target_point.set_data([target_point[0]], [target_point[1]])
        return (line,)

    anim = FuncAnimation(
        fig, animate, init_func=init, frames=200, interval=20, blit=False
    )
    plt.show()
    # TODO: output a csv of the path walked


if __name__ == "__main__":
    main()
