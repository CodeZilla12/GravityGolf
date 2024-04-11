import pygame
import numpy as np
import random
from point_mass import PointMass, generate_pointmass, points_colliding


class Window:
    def __init__(self, screen_size=(800, 800), point_mass_list=None) -> None:
        """_summary_

        Args:
            screen_size (tuple, optional): _description_. Defaults to (800, 800).
            point_mass_list (_type_, optional): _description_. Defaults to None.
        """
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = screen_size

        pygame.init()
        self.SCREEN = pygame.display.set_mode(
            [self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        # sufficiently small arbritrary number. Redefined in main loop.
        self.DELTA_T = 1/self.FPS
        self.TIME_MULT = 3e6

        # self.LOSS_ON_COLLISION = 0.7 #multiplicative
        self.COLLISION_ON = True

        self.G = 6.67e-11  # gravitational constant

        ONE_AU = 1.5e11
        PIXELS_PER_AU = 200

        self.AU_PIXELS_CONVERSION = PIXELS_PER_AU / ONE_AU

        self.SCALE_BAR_FONT = pygame.freetype.Font('COMIC.ttf', 30)

        if not point_mass_list:
            # generate range(N) random pointmasses
            self.object_list = [generate_pointmass(
                (0, self.WINDOW_WIDTH/self.AU_PIXELS_CONVERSION), (0, self.WINDOW_HEIGHT/self.AU_PIXELS_CONVERSION)) for _ in range(20)]
        else:
            self.object_list = point_mass_list

    def draw_scale_bar(self) -> None:
        """_summary_
        """

        ONE_AU = 1.5e11
        x1 = 50
        x2 = x1 + (ONE_AU * self.AU_PIXELS_CONVERSION)

        y = 50
        half_arm_width = 25

        pygame.draw.line(self.SCREEN, (255, 255, 255),
                         (x1, self.WINDOW_HEIGHT-y), (x2, self.WINDOW_HEIGHT-y))
        pygame.draw.line(self.SCREEN, (255, 255, 255), (x1, self.WINDOW_HEIGHT -
                         y-half_arm_width), (x1, self.WINDOW_HEIGHT-y+half_arm_width))
        pygame.draw.line(self.SCREEN, (255, 255, 255), (x2, self.WINDOW_HEIGHT -
                         y-half_arm_width), (x2, self.WINDOW_HEIGHT-y+half_arm_width))
        self.SCALE_BAR_FONT.render_to(self.SCREEN, ((
            x2-x1)/2, self.WINDOW_HEIGHT-y-half_arm_width), '1 AU', (250, 250, 250))

    def main_loop(self) -> None:
        """_summary_
        """
        running = True

        while running:
            self.SCREEN.fill((0, 0, 0))

            self.draw_scale_bar()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for object in self.object_list:

                if object.is_deleted:
                    continue

                pixel_x = object.positions[0] * self.AU_PIXELS_CONVERSION
                pixel_y = self.WINDOW_HEIGHT - \
                    object.positions[1] * self.AU_PIXELS_CONVERSION

                flipped_y_position = np.asarray(
                    [pixel_x, pixel_y])

                pygame.draw.circle(
                    self.SCREEN, object.colour, flipped_y_position, object.radius*self.AU_PIXELS_CONVERSION)

                self.update_object(object)

            for object in self.object_list:
                if object.is_deleted:
                    self.object_list.remove(object)

            # ???
            # do this instead for more precise results
            # for object in self.object_list:
            #    self.update_position(object)

            pygame.display.flip()  # update drawing canvas

            self.DELTA_T = self.CLOCK.tick(self.FPS) * 1e-3
            # self.DELTA_T = 1

    def update_object(self, object: PointMass) -> None:
        """_summary_

        Args:
            object (PointMass): _description_
        """

        """
        ΔVx = GMcos(θ)/(r*t)
        ΔVy = GMsin(θ)/(r*t)
        """

        # The issue with the strong gravity likely lies in how the objects are used in loops.

        for other_object in self.object_list:
            if other_object.id == object.id:  # do not compute force of object on itself
                continue

            if self.COLLISION_ON:
                if points_colliding(object, other_object):

                    other_object.is_deleted = True

                    combined_mass = object.mass + other_object.mass  # absorb other_object into object

                    # object retains its position.

                    object.velocities = (
                        object.mass*object.velocities + other_object.mass*other_object.velocities) / combined_mass

                    object.mass = combined_mass

                    continue

                    # object.attached_point_masses_set.add(other_object)
                    # other_object.is_sub_object = True

                    # coulomb repulsion term. Only occurs on contact. Derive this quantity properly at some point.
                    # repulsion = (9*other_object.collective_mass*1e-19)

                    # object.velocities += - \
                    #     np.sign(object.velocities) * repulsion
                    # other_object.velocities += - \
                    #     np.sign(other_object.velocities) * repulsion

                    # old collision detection
                    # object.velocities = -1 * object.velocities * self.LOSS_ON_COLLISION
                    # other_object.velocities = -1 * object.velocities * self.LOSS_ON_COLLISION

                    # continue  # needed so masses don't slowly sink into each other's center

            dx, dy = other_object.positions - object.positions

            # quadrant-based arctan. Corrects for discrepancies based on sign flipping
            angle = np.arctan2(dy, dx)

            separation = np.hypot(dx, dy)

            # This is the change in velocity due to each object.
            delta_v = (self.G * other_object.mass *
                       self.DELTA_T) / (separation**2)
            delta_vx = delta_v * np.cos(angle) * self.TIME_MULT
            delta_vy = delta_v * np.sin(angle) * self.TIME_MULT

            # [delta_vx, delta_vy]
            object.velocities += np.asarray([delta_vx,
                                            delta_vy], dtype=np.float64)

        object.positions = object.positions + \
            (object.velocities * self.DELTA_T * self.TIME_MULT)


if __name__ == '__main__':

    AU = 1.5e11
    screen_size = (800, 800)
    # Solar system test. Does not work unless 1e6x actual velocities. Gravity too strong.
    # Even then orbits much faster than real-time.
    point_list = [
        # PointMass([0, 0], [2*AU, 3.5*AU], 6e24),
        # PointMass([-5e10, 0], [3*AU, 3.5*AU], 6e24)

        PointMass([-30e3, 0], [2*AU, 3*AU], 6e24),
        PointMass([0, 0], [2*AU, 2*AU], 2e30, colour=(255, 0, 0)),
        PointMass([+30e3, 0], [2*AU, 1*AU], 6e24)
    ]

    # point_list = None

    Window(screen_size, point_list).main_loop()
