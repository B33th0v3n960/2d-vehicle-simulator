from vehicle import Vehicle

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, colors, colormaps

def main() -> None:
    print("==== Testing ====")
    dt = 0.05
    v = 5
    l = 1.6
    duration = 30
    delta = math.pi / 9 
    car = Vehicle(1, 1, math.pi/4, v, l)
    
    xpoints = np.array([])
    ypoints = np.array([])

    test_time = 0
    while (test_time < duration):
        car.update(dt, delta)
        test_time += dt
        print(car)
        xpoints = np.append(xpoints, car.x)
        ypoints = np.append(ypoints, car.y)

    plt.plot(xpoints, ypoints, 'o:r')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
