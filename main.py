import pygame
import numpy as np
import random

class PointMass:
    
    number_of_point_masses = 0

    def __init__(self, velocities:list, positions:list, mass:float, radius = 7e9, colour = (255,255,255) ) -> None:
         
        self.id = PointMass.number_of_point_masses
        PointMass.number_of_point_masses += 1
        
        self.velocities = np.asarray(velocities, dtype = np.float64) 
        self.positions = np.asarray(positions, dtype = np.float64)
        self.mass = mass
        self.radius = radius 
        self.colour = colour

        

class Window:
    def __init__(self,screen_size = (800,800), point_mass_list = None) -> None:
        
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = screen_size
        
        pygame.init()
        self.SCREEN = pygame.display.set_mode([self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.DELTA_T = 1/self.FPS #change this to scale off of frame-time
        
        #self.LOSS_ON_COLLISION = 0.7 #multiplicative
        self.COLLISION_ON = True
        
        self.G = 6.67e-11    #gravitational constant
        
        ONE_AU = 1.5e11
        PIXELS_PER_AU = 200
        
        self.AU_PIXELS_CONVERSION = PIXELS_PER_AU / ONE_AU
            
        self.SCALE_BAR_FONT = pygame.freetype.Font('COMIC.ttf', 30)
        
        if not point_mass_list:
            self.object_list = [self.generate_pointmass() for _ in range(50)] #generate range(N) random pointmasses
        else:
            self.object_list = point_mass_list
        
    
    def generate_pointmass(self, velocities = None, mass = None):
        x = random.randint(0,self.WINDOW_WIDTH/self.AU_PIXELS_CONVERSION)
        y = random.randint(0,self.WINDOW_HEIGHT/self.AU_PIXELS_CONVERSION)
        
        if velocities is None:
            vx = random.randint(-1e5,+1e5)
            vy = random.randint(-1e5,+1e5)
            
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
                
                pygame.draw.circle(self.SCREEN, object.colour, flipped_y_position, object.radius*self.AU_PIXELS_CONVERSION )
            
                self.update_velocity(object)
                
                self.update_position(object)
            
            
            #do this instead for more precise results
            #for object in self.object_list:
            #    self.update_position(object) 
            
            
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
                    
                    repulsion = (9*other_object.mass*1e-19) #coulomb repulsion term. Only occurs on contact. Derive this quantity properly at some point.
                    
                    object.velocities += - np.sign(object.velocities) * repulsion
                    other_object.velocities += - np.sign(other_object.velocities) * repulsion
                    
                    #old collision detection
                    #object.velocities = -1 * object.velocities * self.LOSS_ON_COLLISION
                    #other_object.velocities = -1 * object.velocities * self.LOSS_ON_COLLISION
                    
                    continue #needed so masses don't slowly sink into each other's center
            
            dx,dy = other_object.positions - object.positions
            
            angle = np.arctan2(dy,dx) #quadrant-based arctan. Corrects for discrepancies based on sign flipping 
            
            separation = np.hypot(dx,dy)
            
            object.velocities += np.asarray([
                self.G * other_object.mass * np.cos(angle) / (separation * self.DELTA_T),
                self.G * other_object.mass * np.sin(angle) / (separation * self.DELTA_T)
            ], dtype = np.float64) #[delta_vx, delta_vy]

    

if __name__ == '__main__':
    
    AU = 1.5e11
    screen_size = (800,800)
    #Solar system test. Does not work unless 1e6x actual velocities. Likely to do with the fps.
    point_list = [
    
    PointMass([30e10,-30e10],[2*AU, 3.5*AU], 6e24),
    PointMass([0,0],[2*AU,2*AU], 2e30, colour = (255,0,0)),
    PointMass([-30e10,+30e10],[2*AU, 1*AU], 6e24)
    ]
    
    point_list = None

    Window(screen_size, point_list).main_loop()