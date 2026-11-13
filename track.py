from csv import DictReader
from math import cos, pi, sin
from os import PathLike
from typing import Tuple


class Track:
    @staticmethod
    def circular_track_gen(radius: float, npoints: int) -> list[Tuple[float, float]]:
        """
        generates an array of coordinates in a circle

        npoints: number of points to generate on the track
        """
        track: list[Tuple[float, float]] = []
        d_theta = 2 * pi / npoints
        theta = 0
        track.append((0, 0))
        displacement = radius * sin(d_theta)

        while theta < 2 * pi:
            x = track[-1][0] + displacement * cos(theta)
            y = track[-1][1] + displacement * sin(theta)
            theta += d_theta
            track.append((x, y))

        return track

    @staticmethod
    def s_track_gen(radius: float, npoints: int) -> list[Tuple[float, float]]:
        """
        generates an array of coordinates in a s-shaped track

        npoints: number of points to generate on the track
        """
        track: list[Tuple[float, float]] = []
        d_theta = 2 * pi / npoints
        theta = 0
        track.append((0, 0))
        displacement = radius * sin(d_theta)

        while theta <= pi:
            x = track[-1][0] + displacement * cos(theta)
            y = track[-1][1] + displacement * sin(theta)
            theta += d_theta
            track.append((x, y))

        while theta < 2 * pi:
            x = track[-1][0] + displacement * cos(theta)
            y = track[-1][1] - displacement * sin(theta)
            theta += d_theta
            track.append((x, y))

        return track

    @staticmethod
    def load_csv_track(path: str | PathLike[str]) -> list[Tuple[float, float]]:
        """
        load the track from a csv file
        """
        track: list[Tuple[float, float]] = []
        with open(path, encoding="utf-8") as waypoints:
            reader = DictReader(waypoints, skipinitialspace=True)
            for row in reader:
                try:
                    x = float(row["x"])
                    y = float(row["y"])
                except (KeyError, ValueError, TypeError) as error:
                    raise ValueError(
                        f"Bad waypoint on line {reader.line_num}: {row}"
                    ) from error
                track.append((x, y))
        return track
