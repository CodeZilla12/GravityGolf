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

        # Sufficiently small arbritrary number for first frame. Redefined in main loop.
        self.DELTA_T = 1/self.FPS

        self.TIME_MULT = 1e5
        # self.TIME_MULT = 3e6

        self.COLLISION_ON = True

        self.G = 6.67e-11  # gravitational constant

        self.slingshot_power = 1  # Multiplies the power the slingshot input has
        self.mouse_click_coordinate_pixels = [None, None]

        ONE_AU = 1.5e11
        PIXELS_PER_AU = 200

        self.AU_PIXELS_CONVERSION = PIXELS_PER_AU / ONE_AU

        self.SCALE_BAR_FONT = pygame.freetype.Font('COMIC.ttf', 30)

        # Probably a cleaner way to have this functionality.
        if not point_mass_list:
            # generate range(N) random pointmasses
            self.object_list = [generate_pointmass(
                (0, self.WINDOW_WIDTH/self.AU_PIXELS_CONVERSION), (0, self.WINDOW_HEIGHT/self.AU_PIXELS_CONVERSION)) for _ in range(100)]
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

    def event_handler(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:

                # If escape is pressed when lmb is held down
                if event.key == pygame.K_ESCAPE and pygame.mouse.get_pressed()[0] == True:
                    self.mouse_click_coordinate_pixels = [
                        None, None]  # Cancel action
                    print("Input Cancelled.")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                left_mouse_pressed = pygame.mouse.get_pressed()[0]

                if left_mouse_pressed:

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    self.mouse_click_coordinate_pixels = [mouse_x, mouse_y]

                    au_x = mouse_x / self.AU_PIXELS_CONVERSION
                    au_y = (self.WINDOW_HEIGHT - mouse_y) / \
                        self.AU_PIXELS_CONVERSION

                    # self.object_list.append(
                    # PointMass([0, 0], [au_x,
                    #   au_y], 1e26, 7e9)
                    # )

            elif event.type == pygame.MOUSEBUTTONUP:
                left_mouse_released = not pygame.mouse.get_pressed()[0]

                if left_mouse_released:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    stored_x, stored_y = self.mouse_click_coordinate_pixels

                    # Would only happen if user unclicked mouse button without clicking, or if user cancelled click.
                    if stored_x is None or stored_y is None:
                        break

                    dy = stored_y - mouse_y
                    dx = stored_x - mouse_x

    def main_loop(self) -> None:
        """_summary_
        """
        running = True

        while running:
            self.SCREEN.fill((0, 0, 0))

            self.draw_scale_bar()

            running = self.event_handler()

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

            # Could be a list comprehension / map
            for object in self.object_list:
                if object.is_deleted:
                    self.object_list.remove(object)

            pygame.display.flip()  # update drawing canvas

            self.DELTA_T = self.CLOCK.tick(self.FPS) * 1e-3

    def update_object(self, object: PointMass) -> None:
        """_summary_

        Args:
            object (PointMass): _description_
        """

        """
        ΔVx = GMcos(θ)/(r*t)
        ΔVy = GMsin(θ)/(r*t)
        """

        for other_object in self.object_list:
            if other_object.id == object.id:  # Do not compute force of object on itself
                continue

            if self.COLLISION_ON:
                if points_colliding(object, other_object):

                    larger_object = (object, other_object)[
                        np.argmax((object.mass, other_object.mass))]

                    smaller_object = (object, other_object)[
                        np.argmin((object.mass, other_object.mass))]

                    smaller_object.is_deleted = True

                    combined_mass = object.mass + other_object.mass

                    # Inelastic collision / conservation of momentum
                    larger_object.velocities = (
                        object.mass*object.velocities + other_object.mass*other_object.velocities) / combined_mass

                    larger_object.mass = combined_mass

                    # Smaller object scaled by 1/4 to more accurately model absorption and to limit exponential growth
                    larger_object.radius = larger_object.radius + smaller_object.radius//4

                    # Returns here to avoid unintended behaviour from deleting object. May cause time inaccuracies if low fps or many collisions
                    return

            dx, dy = other_object.positions - object.positions

            # Quadrant-based arctan. Corrects for discrepancies based on sign flipping
            angle = np.arctan2(dy, dx)

            separation = np.hypot(dx, dy)

            # Sums the velocities due to pull from each mass. Same as net forces.
            delta_v = (self.G * other_object.mass *
                       self.DELTA_T) / (separation**2)
            delta_vx = delta_v * np.cos(angle) * self.TIME_MULT
            delta_vy = delta_v * np.sin(angle) * self.TIME_MULT

            object.velocities += np.asarray([delta_vx,
                                            delta_vy], dtype=np.float64)

        # Updates positions with *Net* velocities, hence why outside the loop. Reduces number of calculations per frame.
        object.positions = object.positions + \
            (object.velocities * self.DELTA_T * self.TIME_MULT)


if __name__ == '__main__':

    AU = 1.5e11
    screen_size = (800, 800)

    # Two earths orbiting the sun test
    point_list = [
        PointMass([-30e3, 0], [2*AU, 3*AU], 6e28),
        PointMass([0, 0], [2*AU, 2*AU], 2e30, colour=(255, 0, 0)),
        PointMass([+30e3, 0], [2*AU, 1*AU], 6e24)
    ]

    #
    # point_list = None

    Window(screen_size, point_list).main_loop()
