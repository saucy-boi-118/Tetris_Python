import pygame
from logic import *
from settings import *

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WINW,WINH))
Clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
running = True

# Grid is a 300 by 500, while there is more space for screen
grid:Grid = Grid(WINW,WINH,302)

# First you have a current and next shape
current_peice:Tetrimino = Tetrimino(150,150)
next_peice:Tetrimino = Tetrimino(400,150) # On the side
stored_peice:Tetrimino = Tetrimino(400, 250) # nothing for now
timer = 0

while running:
    # increase timer
    timer += 1

    # Loop through events for input
    for event in pygame.event.get():
        # X button on the screen
        if event.type == pygame.QUIT: 
            running = False
        # Escape button
        elif event.type == pygame.K_ESCAPE:
            running = False
    
    # Keyboard input FOR CURRENT PEICE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: # MOVE LEFT
        current_peice.x_pos -= 1

        # COLLISIONS
        if current_peice.CollisionAnything(grid) or current_peice.CollisionWall(grid):
            current_peice.x_pos += 1

    elif keys[pygame.K_RIGHT]: # MOVE RIGHT
        current_peice.x_pos += 1

        # COLLISIONS
        if current_peice.CollisionAnything(grid) or current_peice.CollisionWall(grid):
            current_peice.x_pos -= 1

    elif keys[pygame.K_UP]: # ROTATE
        if not(current_peice.CollisionWall(grid)) and not(current_peice.CollisionAnything(grid)):
            wall:int = grid.Closest_Wall(current_peice.x_pos) # diff from wall
            current_peice.x_pos -= wall*4
            current_peice.Rotate()

    elif keys[pygame.K_DOWN]:
        if not(current_peice.CollisionWall(grid)) and not(current_peice.CollisionAnything(grid)):
            current_peice.y_pos += 1

    elif keys[pygame.K_s]: # STORING PEICES
        stored_peice, current_peice = current_peice, stored_peice
        current_peice.x_pos = 150 // CELLSIZE
        current_peice.y_pos = 150 // CELLSIZE
        stored_peice.x_pos = 350 // CELLSIZE
        stored_peice.y_pos = 250 // CELLSIZE

    # Clear the screen every frame
    screen.fill(WHITE)

    # Rendering the game

    # Drawing the grid
    grid.Draw_Grid(screen, GREY)

    # Logic and Drawing of the current piece
    if not(current_peice.CollisionWall(grid)) and not(current_peice.CollisionAnything(grid)):
        if timer > 15:
            timer = 0
            current_peice.y_pos += 1 # move down continously
    else:
        current_peice.Print_On_Grid(grid)
        current_peice = next_peice
        next_peice = Tetrimino(400,150)
        current_peice.x_pos = 150 // CELLSIZE
        current_peice.y_pos = 150 // CELLSIZE

    current_peice.Draw_On_Grid(screen, grid) # Draw current
    next_peice.Draw_On_Grid(screen, grid) # Draw the next
    stored_peice.Draw_On_Grid(screen, grid) # draw the stored peice
    grid.ClearLines() # clear the grid lines

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(FPS)

    
pygame.quit()