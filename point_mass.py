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

        self.velocities = np.asarray(velocities, dtype=np.float64)
        self.positions = np.asarray(positions, dtype=np.float64)
        self.mass = mass
        self.radius = radius
        self.colour = colour


def generate_pointmass(xrange, yrange, velocities=None, mass=None) -> PointMass:
    """_summary_

    Args:
        velocities (_type_, list): _description_ List of length two containing x&y velocity respectively. Defaults to None.
        mass (_type_, float): _description_ Mass of the pointmass. Defaults to None.
        None values are randomly generated.

    Returns:
        PointMass: _description_ Returns a PointMass object with random or defined properties based on input.
    """
    x = random.randint(*xrange)
    y = random.randint(*yrange)

    if velocities is None:
        vx = random.randint(-1e5, +1e5)
        vy = random.randint(-1e5, +1e5)

    if velocities:
        vx, vy = velocities

    if mass is None:
        mass = random.randint(10e10, 10e27)

    color = tuple(random.randint(0, 255) for _ in range(3))

    return PointMass([vx, vy], [x, y], mass, colour=color)
