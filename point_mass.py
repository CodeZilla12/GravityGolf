import numpy as np
import random


class PointMass:

    number_of_point_masses = 0

    def __init__(self, velocities: list, positions: list, mass: float, radius=7e9, colour=(255, 255, 255)) -> None:
        """_summary_

        Args:
            velocities (list): _description_
            positions (list): _description_
            mass (float): _description_
            radius (_type_, optional): _description_. Defaults to 7e9.
            colour (tuple, optional): _description_. Defaults to (255, 255, 255).
        """
        self.id = PointMass.number_of_point_masses
        PointMass.number_of_point_masses += 1

        self.is_deleted = False

        self.velocities = np.asarray(velocities, dtype=np.float64)
        self.positions = np.asarray(positions, dtype=np.float64)
        self.mass = mass
        self.radius = radius
        self.colour = colour

    def __del__(self):
        print("Test Del")


def generate_pointmass(xrange=None, yrange=None, velocities=None, mass=None, x=0, y=0) -> PointMass:
    """_summary_

    Args:
        velocities (_type_, list): _description_ List of length two containing x&y velocity respectively. Defaults to None.
        mass (_type_, float): _description_ Mass of the pointmass. Defaults to None.
        None values are randomly generated.

    Returns:
        PointMass: _description_ Returns a PointMass object with random or defined properties based on input.
    """
    if x == 0 and y == 0:
        x = random.randint(*xrange)
        y = random.randint(*yrange)

    if velocities is None:
        vx = random.randint(-1e3, +1e3)
        vy = random.randint(-1e3, +1e3)

    if velocities:
        vx, vy = velocities

    if mass is None:
        mass = random.randint(1e10, 1e30)

    color = tuple(random.randint(0, 255) for _ in range(3))

    return PointMass([vx, vy], [x, y], mass, colour=color)


def points_colliding(point_a: PointMass, point_b: PointMass) -> bool:
    """_summary_

    Args:
        point_a (PointMass): _description_
        point_b (PointMass): _description_

    Returns:
        bool: _description_
    """

    return (point_a.radius - point_b.radius)**2 <= np.sum(np.square(point_a.positions - point_b.positions)) <= (point_a.radius + point_b.radius)**2

    # (R0 - R1)**2 <= (x0 - x1)^2 + (y0 - y1)^2 <= (R0 + R1)^2
