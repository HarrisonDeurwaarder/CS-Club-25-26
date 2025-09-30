import pygame as pg
import sys
from random import randint
import math


WINDOW = (1800, 900)
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
    
    # Set up the playable character
    bird = Bird()
    
    
    '''
    Edit number 1
    
    Make an EMPTY list to store pipes (called it 'pipes')
    Every time a new pipe spawns, we will add it to this list!
    After it gets out of range, we delete it!
    '''
    
    
    # Handle delta time
    clock = pg.time.Clock()
    
    # --- Game Loop --- #
    count = 0
    while True:
        '''
        Edit number 3
        
        Pygame requires us to loop through all of the events going on right now, so let's do that!
        The collection you'll be iterating through is called 'pg.event.get()' (that can be the "list" you iterate through)
        
        Let's say we call every event in pg.event.get() "event"
        '''
        # Loop through all of the events (e.g. buttons, keys, mouse, etc)
        
        # REPLACE THIS COMMENT WITH THE LOOP
            # If the user quits the window
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # If the user presses down a key
            elif event.type == pg.MOUSEBUTTONDOWN:
                bird.jump()
        
        
        '''
        Edit number 2
        
        We want to add a new pipe when the counter variable 'count' is divisible by 60
        This means a new pipe will be added every second (you can change the frequency if you'd like!)
        
        Hint: use the modulo operator to calculate remainder of dividing two numbers
        What would the remainder be if a number is divisible by another?
        
        Then, append this long value expression to 'pipes' to create a new one at a random position:
        Pipe(randint(0, WINDOW[1] - PIPE_GAP))
        '''
        
        
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
        clock.tick(60)
        
        count += 1
        

if __name__ == '__main__':
    main()