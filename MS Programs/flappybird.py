import pygame as pg
import sys
from random import randint
import math


WINDOW = (1500, 700)
PIPE_GAP = 350
PIPE_SPEED = 5

# Colors
BLUE = (190, 245, 245)
BIRD = (100, 100, 100)
PIPE = (0, 255, 0)

# Images

BIRD_SIZE = (75, 50)
PIPE_SIZE = (100, 1500)

bird_img = pg.image.load('MS Programs\FBImages\\bird.png')
bird_img = pg.transform.scale(bird_img, BIRD_SIZE)
bird_angle = 0

pipe_img = pg.image.load('MS Programs\FBImages\\pipe.png')
pipe_img = pg.transform.scale(pipe_img, PIPE_SIZE)
pipe_mask = pg.mask.from_surface(pipe_img)


class Pipe:
    '''
    The pipe obstacle
    '''
    def __init__(self,
                 start_depth: int = 0,) -> None:
        self.start = start_depth
        self.pos = WINDOW[0]
        
    def step(self,) -> None:
        '''
        Idly updates the pipe's position
        '''
        self.pos -= PIPE_SPEED
    
    def draw(self,
             screen: pg.Surface) -> None:
        '''
        Draw the bird at the given position
        '''
        # Draw the bottom pipe
        screen.blit(pipe_img, (self.pos, self.start + PIPE_GAP))
        
        # Draw the top pipe
        screen.blit(pg.transform.rotate(pipe_img, 180), (self.pos, self.start - PIPE_SIZE[1]))
    

class Bird:
    '''
    The playable bird
    '''
    def __init__(self,) -> None:
        self.pos = WINDOW[1] // 2
        self.vel = 0.0
        
    def jump(self,
             power: float = 10.0,) -> None:
        '''
        Updates the bird's velocity to account for a jump
        '''
        self.vel = power
    
    def step(self,
             gravity: float = 0.4) -> None:
        '''
        Idly updates the bird's velocity and its position
        '''
        # Position update
        self.pos -= self.vel
        # Ensure the bird is in the bounds of the game
        self.pos = 0 if self.pos < 0 else self.pos
        self.pos = WINDOW[1] - BIRD_SIZE[1] if self.pos > WINDOW[1] - BIRD_SIZE[1] else self.pos
        # Velocity update
        self.vel -= gravity
         
    def draw(self,
             screen: pg.Surface) -> None:
        '''
        Draw the bird at the given position
        '''
        screen.blit(
            pg.transform.rotate(bird_img, math.atan(self.vel/10)*50), 
            (100, self.pos),
        )
    
    
def main() -> None:
    '''
    Main function
    '''
    # Pygame initialization
    pg.init()
    # Set up the window
    screen = pg.display.set_mode(WINDOW,)
    pg.display.set_caption('Flappy Bird Game',)
    
    # Set up the playable character and the list of pipes
    bird = Bird()
    pipes: list[Pipe] = []
    
    # Handle delta time
    clock = pg.time.Clock()
    
    # --- Game Loop --- #
    count = 0
    while True:
        # Loop through all of the events (e.g. buttons, keys, mouse, etc)
        for event in pg.event.get():
            # If the user quits the window
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # If the user presses down a key
            elif event.type == pg.MOUSEBUTTONDOWN:
                bird.jump()
        
        # Frequently add new pipes
        if count % 70 == 0:
            pipes.append(Pipe(randint(0, WINDOW[1] - PIPE_GAP)))
        
        # Fill the background
        screen.fill(BLUE,)
        
        # Update the motion and positions
        bird.step()
        bird.draw(screen,)
        
        # The mask checks for collisions
        bird_mask = pg.mask.from_surface(pg.transform.rotate(bird_img, math.atan(bird.vel/10)*50))
        
        for i, pipe in enumerate(pipes):
            # Check if the pipe is beyond the screen
            if pipe.pos <= -PIPE_SIZE[0]:
                pipes.pop(i)
                
            # Update the motion
            pipe.step()
            pipe.draw(screen,)
            
            # Check for collision
            offset_top = (pipe.pos - 100, (pipe.start - PIPE_SIZE[1]) - bird.pos)
            offset_bottom = (pipe.pos - 100, (pipe.start + PIPE_GAP) - bird.pos)
            if bird_mask.overlap(pipe_mask, offset_bottom) or bird_mask.overlap(pipe_mask, offset_top):
                main()
        
        # Update the display with all the changes made
        pg.display.flip()
        
        # Limit update rate to 80fps
        clock.tick(80)
        
        count += 1
        

if __name__ == '__main__':
    main()