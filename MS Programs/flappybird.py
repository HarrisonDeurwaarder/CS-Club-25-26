import pygame as pg
import sys
from random import randint


WINDOW = (1000, 500)
PIPE_GAP = 150
PIPE_SPEED = 5

# Colors
BLUE = (190, 245, 245)
BIRD = (100, 100, 100)
PIPE = (0, 255, 0)


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
        print(self.pos)
        # Draw the top pipe
        pg.draw.rect(screen,
                     PIPE,
                     pg.Rect(self.pos, 0, 20, self.start))
        # Draw the bottom pipe
        pg.draw.rect(screen,
                     PIPE,
                     pg.Rect(self.pos, self.start + PIPE_GAP, 20, WINDOW[1] - self.start + PIPE_GAP))
    

class Bird:
    '''
    The playable bird
    '''
    def __init__(self,) -> None:
        self.pos = WINDOW[1] // 2
        self.vel = 0.0
        
    def jump(self,
             power: float = 7.0,) -> None:
        '''
        Updates the bird's velocity to account for a jump
        '''
        self.vel = power
    
    def step(self,
             gravity: float = 0.2) -> None:
        '''
        Idly updates the bird's velocity and its position
        '''
        # Position update
        self.pos -= self.vel
        # Velocity update
        self.vel -= gravity
         
    def draw(self,
             screen: pg.Surface) -> None:
        '''
        Draw the bird at the given position
        '''
        pg.draw.circle(screen,
                       BIRD,
                       (100, self.pos),
                       radius=20,)
    
    
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
        
        for i, pipe in enumerate(pipes):
            # Check if the pipe is beyond the screen
            if pipe.pos <= -10:
                pipes.pop(i)
            # Update the motion
            pipe.step()
            pipe.draw(screen,)
        
        # Update the display with all the changes made
        pg.display.flip()
        
        # Limit update rate to 60fps
        clock.tick(60)
        
        count += 1
        

if __name__ == '__main__':
    main()