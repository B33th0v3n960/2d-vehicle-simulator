from math import pi, cos, sin
from typing import Tuple

class Track:
    @staticmethod
    def circular_track_gen(radius: float, npoints: int) -> list[Tuple[float, float]]:
        track: list[Tuple[float, float]] = []
        d_theta = 2 * pi / npoints
        theta = 0
        track.append((0, 0))
        displacement = radius * sin(d_theta)

        while (theta < 2 * pi):
            x = track[-1][0] + displacement * cos(theta)
            y = track[-1][1] + displacement * sin(theta)
            theta += d_theta
            track.append((x, y))

        return track

    @staticmethod
    def s_track_gen(radius: float, npoints: int) -> list[Tuple[float, float]]:
        track: list[Tuple[float, float]] = []
        d_theta = 2 * pi / npoints
        theta = 0
        track.append((0, 0))
        displacement = radius * sin(d_theta)

        while (theta < pi):
            x = track[-1][0] + displacement * cos(theta)
            y = track[-1][1] + displacement * sin(theta)
            theta += d_theta
            track.append((x, y))
        
        temp_y = [track[-1][1]]
        while (theta < 2 * pi):
            x = track[-1][0] + displacement * cos(theta)
            y = temp_y[-1] + displacement * sin(theta)
            temp_y.append(y)
            theta += d_theta
            track.append((x, -temp_y[-1]))

        return track
