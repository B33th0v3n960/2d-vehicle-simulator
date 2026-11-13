from math import atan, atan2, sin, sqrt
from typing import Tuple

from vehicle import Vehicle


class Control:
    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """
        distance between (x1, y1) to (x2, y2)
        """
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def steer_car(car: Vehicle, ld: float, target_point: Tuple[float, float]) -> float:
        """
        return delta the amount to steer, to get to target_point
        """
        delta_x = target_point[0] - car.x
        delta_x = (delta_x) if abs(delta_x) > 0.001 else 0.001
        alpha = atan2((target_point[1] - car.y), delta_x) - car.yaw
        delta = atan2(2 * car.wheelbase * sin(alpha), ld)
        return delta
