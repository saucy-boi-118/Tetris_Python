import pygame
from logic import *
from settings import *

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WINW,WINH))
Clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
running = True

# Grid with partition
grid:Grid = Grid(WINW,WINH,302)

# First you have a current and next shape
current_peice:Tetrimino = Tetrimino(150,150)
next_peice:Tetrimino = Tetrimino(400,150) # On the side
stored_peice:Tetrimino = Tetrimino(400, 250) # nothing for now
timer = 0

# Game over
font = pygame.font.SysFont("impact",32)
font.bold = True
# GAME VOER
game_over_text = font.render("GAMEOVER", True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINW // 2, WINH//2 + 50)
# RESTART
restart_text = font.render("SPACE TO RESTART", True, GREEN)
restart_rect = restart_text.get_rect()
restart_rect.center = (WINW // 2, WINH//2  - 50)
# SCORE
font = pygame.font.SysFont("impact",20)
font.bold = True
score:int = 0
score_text = font.render(f"SCORE: {score}", True, WHITE)
score_rect = score_text.get_rect()
score_rect.center = (100,40)

# Game looping variables
game_over = False

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

    # Game is running
    if game_over == False:
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
            # If its not colliding with anything
            if not(current_peice.CollisionAnything(grid)):   

                current_peice.Rotate() # First rotate the peice

                # Check if it collided with the wall and if it did displace it
                if current_peice.CollisionWall(grid):
                    wall:int = grid.Closest_Wall(current_peice.x_pos) # diff from wall
                    current_peice.x_pos -= wall*4

        elif keys[pygame.K_DOWN]: # HARD DROPPING
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
            # Check if the peice is in the lose state
            if current_peice.y_pos < 8:
                game_over = True
            current_peice.Print_On_Grid(grid)
            current_peice = next_peice
            next_peice = Tetrimino(400,150)
            current_peice.x_pos = 150 // CELLSIZE
            current_peice.y_pos = 150 // CELLSIZE

        current_peice.Draw_On_Grid(screen, grid) # Draw current

        next_peice.Draw_On_Grid(screen, grid) # Draw the next

        stored_peice.Draw_On_Grid(screen, grid) # draw the stored peice

        score += grid.ClearLines() # clear the grid lines

        while grid.AnyEmptyLine(): # if there is any empty lines 
            grid.MoveLines() # Move them

        score += grid.ClearLines() # Clear the lines agains

        # DRAWING SCORE
        screen.blit(score_text, score_rect)

    else:
        screen.fill(BLACK)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        # Space for restart
        if keys[pygame.K_SPACE]:
            game_over = False

            # Restarting
            grid.ClearGrid()

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(FPS)

    
pygame.quit()