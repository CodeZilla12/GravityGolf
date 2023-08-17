import pygame
import numpy as np

class Window:
    def __init__(self):
        
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 400
        
        self.object_list = [[0,np.asarray([0,0]),np.asarray([50,50]), 10],
                            [1,np.asarray([0,0]),np.asarray([750,350]), 10]
        ] #sublists give id int,velocity(vx,vy) numpy, position(x,y) numpy, mass(m) numlike
        
        pygame.init()
        self.SCREEN = pygame.display.set_mode([self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DELTA_T = 1/self.FPS #change this to scale off of frame-time
        
        self.G = 6.67e-11    
        
    def main_loop(self):
        
        running = True
        self.SCREEN.fill((0,0,0))
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            
            
            for i,object in enumerate(self.object_list):
                position = [object[2][0], self.WINDOW_HEIGHT - object[2][1]] #refactor this
                
                pygame.draw.circle(self.SCREEN, np.asarray([255,255,255])/(i+1), position, 10 )
            
            
            for object in self.object_list:
                self.update_velocity(object)
                self.update_position(object)
            
            
            pygame.display.flip()
            
            self.CLOCK.tick(30)
    
    def update_position(self,object):
        id, velocities, positions, _mass = object #refactor as dictionary
        
        positions = positions + velocities * self.DELTA_T
        
        self.object_list[id] = [id, velocities, positions, _mass]
    
    def update_velocity(self,object):
        id, velocities, positions, _mass = object
        
        """
        ΔVx = GMcos(θ)/(r*t)
        ΔVy = GMsin(θ)/(r*t)
        """
        
        delta_velocities = np.asarray([0,0])
        delta_t = 1/self.FPS #change to real delta_t
        
        for other_object in self.object_list:
            other_id,_,other_positions,other_mass = object
            if other_id == id:
                continue
                
            dx,dy = other_positions - positions
            
            angle = np.arctan(dx/dy)
            separation = np.hypot(dx,dy)
            
            delta_velocities += np.asarray([
                self.G * other_mass * np.cos(angle) / (separation * self.DELTA_T),
                self.G * other_mass * np.sin(angle) / (separation * self.DELTA_T)
            ]) #[delta_vx, delta_vy]
            
        velocities += np.asarray([10,10])
        self.object_list[id] = [id,velocities,positions,_mass]
        return
        
        velocities += delta_velocities
        
        self.object_list[id] = [id,velocities,positions,_mass]
    

if __name__ == '__main__':
    Window().main_loop()