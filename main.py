import pygame
import numpy as np
import random

class PointMass:
    
    number_of_points = 0

    def __init__(self, velocities, positions, mass, radius = 10, colour = (255,255,255) ):
         
        self.id = PointMass.number_of_points
        PointMass.number_of_points += 1
        
        self.velocities = np.asarray(velocities, dtype = np.float64) 
        self.positions = np.asarray(positions, dtype = np.float64)
        self.mass = mass
        self.radius = radius 
        self.colour = colour

        

class Window:
    def __init__(self, point_mass_list = None):
        
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        
        if not point_mass_list:
            self.object_list = [self.generate_pointmass() for _ in range(2)] #generate range(N) random pointmasses
        else:
            self.object_list = point_mass_list
        
        pygame.init()
        self.SCREEN = pygame.display.set_mode([self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DELTA_T = 1/self.FPS #change this to scale off of frame-time
        self.LOSS_ON_COLLISION = 0.4 #multiplicative
        self.COLLISION_ON = True
        
        self.G = 6.67e-11    #gravitational constant
        
        ONE_AU = 1.5e11
        PIXELS_PER_AU = 50
        
        self.AU_PIXELS_CONVERSION = PIXELS_PER_AU / ONE_AU
        
        for object in self.object_list: #temp fix. change unit tests
            object.positions /= self.AU_PIXELS_CONVERSION
            
        self.SCALE_BAR_FONT = pygame.freetype.Font('COMIC.ttf', 30)
        
    
    def generate_pointmass(self, velocities = None, mass = None):
        x = random.randint(0,self.WINDOW_WIDTH)
        y = random.randint(0,self.WINDOW_HEIGHT)
        
        if velocities is None:
            vx = random.randint(-100,100)
            vy = random.randint(-100,100)
            
        if velocities:
            vx,vy = velocities
        
        if mass is None:
            mass = random.randint(10e10,10e27)
        
        color = tuple(random.randint(0,255) for _ in range(3))
        
        return PointMass([vx,vy],[x,y], mass, colour = color)
        
    @staticmethod
    def points_colliding(point_a, point_b):
        
        return (point_a.radius - point_b.radius)**2 <= np.sum(np.square(point_a.positions - point_b.positions)) <= (point_a.radius + point_b.radius)**2
        
        #(R0 - R1)**2 <= (x0 - x1)^2 + (y0 - y1)^2 <= (R0 + R1)^2
    
    def draw_scale_bar(self):
    
        x1 = 50
        x2 = x1 + (1.5e11 * self.AU_PIXELS_CONVERSION)
    
        y = 50
        half_arm_width = 25
        
        pygame.draw.line(self.SCREEN, (255,255,255), (x1,self.WINDOW_HEIGHT-y), (x2 ,self.WINDOW_HEIGHT-y) )
        pygame.draw.line(self.SCREEN, (255,255,255), (x1,self.WINDOW_HEIGHT-y-half_arm_width), (x1 ,self.WINDOW_HEIGHT-y+half_arm_width) )
        pygame.draw.line(self.SCREEN, (255,255,255), (x2,self.WINDOW_HEIGHT-y-half_arm_width), (x2 ,self.WINDOW_HEIGHT-y+half_arm_width) )
        self.SCALE_BAR_FONT.render_to(self.SCREEN, ((x2-x1)/2, self.WINDOW_HEIGHT-y-half_arm_width), '1 AU', (250, 250, 250))
    
    def main_loop(self):
        
        running = True
        
        while running:
            self.SCREEN.fill((0,0,0))
            
            self.draw_scale_bar()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            
            for object in self.object_list:
                
                flipped_y_position = np.asarray( [object.positions[0] * self.AU_PIXELS_CONVERSION, self.WINDOW_HEIGHT - object.positions[1] * self.AU_PIXELS_CONVERSION] ) #refactor this
                
                pygame.draw.circle(self.SCREEN, object.colour, flipped_y_position, object.radius )
            
                self.update_velocity(object)
                self.update_position(object) #Updating position here will cause inaccuraccy at small separation / high mass. Ideally in its own loop?
            
            
            pygame.display.flip()
            
            self.CLOCK.tick(30)
            
    
    def update_position(self,object):
    
        object.positions = object.positions + (object.velocities * self.DELTA_T)
        
        
    def update_velocity(self,object):

        """
        ΔVx = GMcos(θ)/(r*t)
        ΔVy = GMsin(θ)/(r*t)
        """
        
        for other_object in self.object_list:
            if other_object.id == object.id: #do not compute force of object on itself
                continue
            
            if self.COLLISION_ON:
                if self.points_colliding(object,other_object):
                    object.velocities = -1 * object.velocities * self.LOSS_ON_COLLISION
                    return
            
            dx,dy = other_object.positions - object.positions
            
            angle = np.arctan2(dy,dx) #quadrant-based arctan. Corrects for discrepancies based on sign flipping 
            
            separation = np.hypot(dx,dy)
            
            object.velocities += np.asarray([
                self.G * other_object.mass * np.cos(angle) / (separation * self.DELTA_T),
                self.G * other_object.mass * np.sin(angle) / (separation * self.DELTA_T)
            ], dtype = np.float64) #[delta_vx, delta_vy]

    

if __name__ == '__main__':
    
    """
    point_list = [PointMass([0,0],[200,300], 10),
                            PointMass([0,0],[500,300], 10),
                            PointMass([0,0],[600,300], 10e10),
                            PointMass([0,0],[200,400], 10),
                            PointMass([0,0],[600,400], 10)            
        ]
    """
    
    #point_list = [PointMass([50,0],[200,300],10),PointMass([0,0],[400,300],10)] #Collision test


    #point_list = [PointMass([50,0],[100,100],10e10),PointMass([0,0],[400,400],10e11,colour = (255,0,0))]
    
    point_list = None

    Window(point_list).main_loop()