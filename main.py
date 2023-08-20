import pygame
import numpy as np
import random

class PointMass:
    
    number_of_points = 0

    def __init__(self, velocities, positions, mass, radius = 10, colour = (255,255,255) ):
         
        self.id = PointMass.number_of_points
        PointMass.number_of_points += 1
        
        self.velocities = np.asarray(velocities, dtype = np.float64) 
        self.positions = np.asarray(positions, dtype = np.int32)
        self.mass = mass
        self.radius = radius 
        self.colour = colour
        

class Window:
    def __init__(self, point_mass_list = None):
        
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        
        #could move this into the PointMass class
        
        """
        self.object_list = [PointMass([0,0],[200,300], 10),
                            PointMass([0,0],[500,300], 10),
                            PointMass([0,0],[600,300], 10e10),
                            PointMass([0,0],[200,400], 10),
                            PointMass([0,0],[600,400], 10)            
        ]
        """
        
        if not point_mass_list:
            self.object_list = [self.generate_pointmass([0,0],10e10) for _ in range(50)] #generate range(N) random pointmasses
        else:
            self.object_list = point_mass_list
        
        pygame.init()
        self.SCREEN = pygame.display.set_mode([self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DELTA_T = 1/self.FPS #change this to scale off of frame-time
        
        self.G = 6.67e-11    
    
    def generate_pointmass(self, velocities = None, mass = None):
        x = random.randint(0,self.WINDOW_WIDTH)
        y = random.randint(0,self.WINDOW_HEIGHT)
        
        if velocities is None:
            vx = random.randint(-10,10)
            vy = random.randint(-10,10)
            
        if velocities:
            vx,vy = velocities
        
        if mass is None:
            mass = random.randint(10,1e10)
        
        color = tuple(random.randint(0,255) for _ in range(3))
        
        return PointMass([vx,vy],[x,y], mass, colour = color)
        
        
    def main_loop(self):
        
        running = True
        
        while running:
            self.SCREEN.fill((0,0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            
            for object in self.object_list:
                
                flipped_y_position = [object.positions[0], self.WINDOW_HEIGHT - object.positions[1]] #refactor this
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
                
            dx,dy = other_object.positions - object.positions
            
            angle = np.arctan2(dy,dx) #quadrant-based arctan. Corrects for discrepancies based on sign flipping 
            
            separation = np.hypot(dx,dy)
            
            object.velocities += np.asarray([
                self.G * other_object.mass * np.cos(angle) / (separation * self.DELTA_T),
                self.G * other_object.mass * np.sin(angle) / (separation * self.DELTA_T)
            ], dtype = np.float64) #[delta_vx, delta_vy]

    

if __name__ == '__main__':
    Window().main_loop()