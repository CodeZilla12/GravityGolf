import numpy as np


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
