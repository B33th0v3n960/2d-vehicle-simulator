from math import cos, sin, tan, pi


class Vehicle:

    def __init__(
        self, x: float, y: float, yaw: float, velocity: float, wheelbase: float
    ) -> None:
        """
        Vehicle contructor

        yaw: rotation around the y-axis (radians)
        wheelbase: distance between front centre to back wheel centre
        """
        self.x = x
        self.y = y
        self.yaw = yaw
        self.velocity = velocity
        self.wheelbase = wheelbase

    def update(self, dt: float, delta: float) -> None:
        """
        update the state of the vehicle

        dt: simulation time step
        delta: front wheel steering angle

        delta_lim = pi/3
        """
        delta_lim = pi/3
        delta = max(delta, -delta_lim)
        delta = min(delta, delta_lim)
        self.x = self.x + self.velocity * cos(self.yaw) * dt
        self.y = self.y + self.velocity * sin(self.yaw) * dt
        self.yaw = self.yaw + (self.velocity / self.wheelbase) * tan(delta) * dt

    def __str__(self):
        return (
            f"Car: ({self.x}, {self.y}),"
            f"yaw: {self.yaw},"
            f"velocity: {self.velocity},"
            f"wheelBase: {self.wheelbase}"
        )
