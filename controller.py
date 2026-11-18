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
        dr = max(dr, 0.001)
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

    target_pt: point_t = (0, 0)

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
        minX = min(pt1[0], pt2[0])
        minY = min(pt1[1], pt2[1])
        maxX = max(pt1[0], pt2[0])
        maxY = max(pt1[1], pt2[1])
        dist_pt2_target1 = __class__.distance(pt2, target_point1)
        dist_pt2_target2 = __class__.distance(pt2, target_point2)
        dist_pt1_car = __class__.distance(pt1, current_pos)
        dist_pt2_car = __class__.distance(pt2, current_pos)

        if not intersection_found:
            return __class__.point_to_line_seg(current_pos, pt1, pt2)

        target1_x_inbound = minX <= target_point1[0] <= maxX
        target1_y_inbound = minY <= target_point1[1] <= maxY
        target1_inbound = target1_x_inbound and target1_y_inbound
        target2_x_inbound = minX <= target_point2[0] <= maxX
        target2_y_inbound = minY <= target_point2[1] <= maxY
        target2_inbound = target2_x_inbound and (target2_y_inbound)

        if target1_inbound and target2_inbound:
            return (
                target_point1
                if (dist_pt2_target1 < dist_pt2_target2)
                else target_point2
            )
        if target1_inbound:
            return target_point1
        if target2_inbound:
            return target_point2
        return pt1 if dist_pt1_car < dist_pt2_car else pt2

    @staticmethod
    def point_to_line_seg(current_pos: point_t, pt1: point_t, pt2: point_t) -> point_t:
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        denominator = dx**2 + dy**2
        if denominator == 0:
            return pt1
        numerator = (current_pos[0] - pt1[0]) * dx + (current_pos[1] - pt1[1]) * dy
        t = max(0.0, min(numerator / denominator, 1.0))
        return (pt1[0] + t * dx, pt1[1] + t * dy)
