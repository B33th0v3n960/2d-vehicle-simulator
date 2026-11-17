from math import atan, atan2, sin, sqrt
from typing import Tuple

from vehicle import Vehicle

point_t = Tuple[float, float]


class Control:
    @staticmethod
    def distance(pt1: point_t, pt2: point_t) -> float:
        """
        distance between pt1 to pt2
        """
        return sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

    @staticmethod
    def steer_car(car: Vehicle, ld: float, target_point: point_t) -> float:
        """
        return delta the amount to steer, to get to target_point
        """
        delta_x = target_point[0] - car.x
        delta_x = (delta_x) if abs(delta_x) > 0.001 else 0.001
        alpha = atan2((target_point[1] - car.y), delta_x) - car.yaw
        delta = atan2(2 * car.wheelbase * sin(alpha), ld)
        return delta

    @staticmethod
    def sgn(num):
        """
        return the sign of the number
        """
        if num >= 0:
            return 1
        else:
            return -1

    @staticmethod
    def line_circle_intersection(
        current_pos: point_t, look_ahead_dist: float, pt1: point_t, pt2: point_t
    ) -> Tuple[point_t, point_t, bool]:
        """
        compute the intersection between the line `pt1` -> `pt2`, to the circle
        around `current_pos` with the radius of `look_ahead_dist`
        """
        intersection_found = False
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        dr = sqrt(dx**2 + dy**2)
        if dr <= 0.001:
            dr = 0.001
        x1_offset = pt1[0] - current_pos[0]
        y1_offset = pt1[1] - current_pos[1]
        x2_offset = pt2[0] - current_pos[0]
        y2_offset = pt2[1] - current_pos[1]
        d = x1_offset * y2_offset - x2_offset * y1_offset

        discriminant = look_ahead_dist**2 * dr**2 - d**2

        if discriminant < 0:
            return (0, 0), (0, 0), False

        x1 = (d * dy + __class__.sgn(dy) * dx * sqrt(discriminant)) / dr**2
        y1 = (-d * dx + abs(dy) * sqrt(discriminant)) / dr**2
        x2 = (d * dy - __class__.sgn(dy) * dx * sqrt(discriminant)) / dr**2
        y2 = (-d * dx - abs(dy) * sqrt(discriminant)) / dr**2

        return (
            (x1 + current_pos[0], y1 + current_pos[1]),
            (x2 + current_pos[0], y2 + current_pos[1]),
            True,
        )

    @staticmethod
    def get_target_point(
        current_pos: point_t, look_ahead_dist: float, pt1: point_t, pt2: point_t
    ) -> point_t:
        """
        computes the target point given 2 points and look_ahead_dist
        travelling from `pt1` to `pt2`
        """
        target_point1, target_point2, intersection_found = (
            __class__.line_circle_intersection(
                current_pos,
                look_ahead_dist,
                pt1,
                pt2,
            )
        )

        if not intersection_found:
            return pt1

        dist_point1 = __class__.distance(pt2, target_point1)
        dist_point2 = __class__.distance(pt2, target_point2)
        if dist_point1 >= dist_point2:
            return target_point2
        return target_point1
