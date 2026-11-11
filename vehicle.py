import math


class Vehicle:

    # Vehicle contructor
    #
    # param:
    #   x :
    #   y :
    #   yaw: rotation around the y-axis (radians)
    #   v: velocity
    #   l: wheelBase - distance between front centre to back wheel centre
    def __init__(self, x: float, y: float, yaw: float, v: float, l: float) -> None:
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.l = l

    # update()
    #
    # update the state of the vehicle
    #
    # param:
    #   dt: simulation time step
    #   delta: front wheel steering angle
    def update(self, dt: float, delta: float) -> None:
        self.x = self.x + self.v * math.cos(self.yaw) * dt
        self.y = self.y + self.v * math.sin(self.yaw) * dt
        self.yaw = self.yaw + (self.v / self.l) * math.tan(delta) * dt

    def __str__(self):
        return (
            f"Car: ({self.x}, {self.y}),"
            f"yaw: {self.yaw},"
            f"velocity: {self.v},"
            f"wheelBase: {self.l}"
        )
