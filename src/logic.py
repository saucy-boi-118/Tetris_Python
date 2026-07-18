import pygame
from settings import *
import numpy as np
import random as r

# Colors that map to each tetrimino
colors:list[pygame.Color] = [
    CYAN, # STRAIGHT TETRIMINO // 0
    YELLOW, # SQUARE TETRIMINO // 1
    PINK, # T - TETRIMINO // 2
    ORANGE, # L - TETRIMINO // 3
    BLUE, # J - TETRIMINO // 4
    RED, # Z - TETRIMINO // 5
    GREEN, # S - TETRIMINO // 6
    BLACK, # EMPTY // 7
]
# Grid class for the base
class Grid:
    def __init__(self, width:int, height:int, partition:int):

        # Create a 1d array of zeros and reshape it into a 2d arry for the grid
        self.height = height // CELLSIZE
        self.width = width // CELLSIZE
        self.cellsize = CELLSIZE
        self.partition = partition // CELLSIZE
        self.game_width = self.width - (self.width - self.partition)
        self.grid = np.ones(width*height, dtype=int).reshape(height, width) * 7

        # Creating a border for the map
        # Left is rows, Right is columns

        # Left and Right Rows
        # For all the rows for every (width-1) columns set it to 1
        self.grid[:self.height, ::self.width-1] = 8

        # Top and Bottom Rows
        # For every (height-1) rows for every column set it to 1
        self.grid[::self.height-1, :self.width] = 8

        # FOR THE PARTITIONS
        self.grid[:self.height, self.game_width:] = 8 
    def Draw_Grid(self, screen:pygame.Surface, border_color:pygame.Color) -> None:
        # Loop through the grid and draw it for each square
        self.__Redefine()
        for i in range(self.height):
            for j in range(self.width):

                # Variable for the cell rectangle
                cell_rect:pygame.Rect = pygame.Rect(j*self.cellsize, i*self.cellsize, self.cellsize, self.cellsize)

                # drawing each rectangle
                if self.grid[i,j] == 8:
                    self.grid[i,j] = 8 # Once a border always a border
                    pygame.draw.rect(screen, border_color, cell_rect)
                else:
                    # Get the index for the colors 
                    value:int = self.grid[i,j]

                    # Draw to that color value
                    pygame.draw.rect(screen, colors[value], cell_rect) 
    def Set_Grid_Value(self, row:int, column:int, value:int) -> None:
        # Setting a grid coordinate to a value
        self.grid[row, column] = value
    def Is_Grid_Value(self, row:int, column:int, value:int) -> bool:
        if self.grid[row, column] == value:
            return True
        
        return False
    def Is_Grid_Value_Range(self, row:int, column:int, min:int, max:int) -> bool:
        grid_value = self.grid[row, column]

        # is the value in between the min and the max
        if min <= grid_value <= max:
            return True

        return False
    def Closest_Wall(self, column:int) -> int:
        # Get the distances between walls
        # Left distance is just the columns - 0
        right_dist:int = self.game_width - column

        # If the distance to the left wall if shorter than the right 
        if column < right_dist and right_dist < 20:
            return -1 # return left
        else:
            # Return right
            return 1
    def ClearLines(self):
        for i in range(self.height-2,15,-1):

            # A list of the amount of empty spaces
            row = self.grid[i]
            result = [x for x in range(1,self.game_width) if(lambda x: row[x]==7)(x)]

            # If its not empty
            if len(result) == 0 or len(result) == self.game_width:
                # Clear the row
                row[1:self.game_width] = 7

                # loop through the rows
                # set the current row to the previous one
                for i in range(self.height-1,15,-1):
                    previous_row = self.grid[i-1]
                    self.grid[i] = previous_row
    def __Redefine(self):
        # Left and Right Rows
        # For all the rows for every (width-1) columns set it to 1
        self.grid[:self.height, ::self.width-1] = 8

        # Top and Bottom Rows
        # For every (height-1) rows for every column set it to 1
        self.grid[::self.height-1, :self.width] = 8

        # FOR THE PARTITIONS
        self.grid[:self.height, self.game_width:] = 8 
# Class for each piece, called a tetrimino
class Tetrimino:
    # All the shapes with their rotations
    shapes:list[list[list[int]]] = [

        #| STRAIGHT -----| | FACING UP ------|
        [[1,0,2,0,3,0,4,0],[0,-2,0,-1,0,0,0,1]], # STRAIGHT TETRIMINO - 2 ROTATIONS
        
        #| JUST A SQUARE |
        [[0,0,1,0,0,1,1,1]], # SQUARE TETRIMINO - 1 ROTATIONS

        #|NORMAL---------| |UPSIDE DOWN-----| |FACING RIGHT---| |FACING LEFT------|
        [[0,0,1,0,2,0,1,1],[0,0,1,0,2,0,1,-1],[0,0,0,1,0,2,1,1],[0,0,0,1,0,2,-1,1]], # T - TETRIMINO - 4 ROTATIONS

        #|NORMAL-----------| |FACING DOWN----| |FACING UP------| |FLIPPED RIGHT--|
        [[0,0,0,1,0,2,-1,2],[0,0,1,0,2,0,2,1],[0,0,0,1,1,1,2,1],[0,0,1,0,0,1,0,2]], # L - TETRIMINO - 4 ROTATIONS

        #|NORMAL---------| |FACING UP--------| |FLIPPED RIGHT--| |FACING DOWN----|
        [[0,0,1,0,1,1,-1,0],[0,0,0,1,-1,1,-2,1],[0,0,0,1,0,2,1,2],[0,0,0,1,1,0,2,0]], # j - TETRIMINO - 4 ROTATIONS

        #|NORMAL---------| |UP---------------|
        [[0,0,1,0,1,1,2,1],[0,0,0,1,-1,1,-1,2]], # SKEW: Z - TETRIMINO - 2 ROTATIONS

        #|NORMAL------------| |UP-------------| 
        [[0,0,-1,0,-1,1,-2,1],[0,0,0,1,1,1,1,2]], # SKEW: S - TETRIMINO - 2 ROTATIONS 
        
    ]
    # HOW TO DEFINE A SHAPE
    # SHAPE = shapes[TYPE_OF_TETRIMINO][TYPE_OF_ROTATION][POSITION]
    def __init__(self, x_pos:int, y_pos:int) -> None:

        # position
        self.x_pos:int = x_pos // CELLSIZE
        self.y_pos:int = y_pos // CELLSIZE

        # shape, choose a random shape with rotation
        self.type_of_shape = r.randint(0,len(self.shapes)-1) # What type is it
        self.current_rotation:int = 0 # First rotation
        self.current_shape:list[int] = self.shapes[self.type_of_shape][self.current_rotation]
    def Rotate(self) -> None:
        self.current_rotation += 1 # increase rotation
        self.current_rotation %= len(self.shapes[self.type_of_shape]) # Loop it around the length of shape
        self.current_shape = self.shapes[self.type_of_shape][self.current_rotation]
    # Draw it on the grid
    def Print_On_Grid(self, grid:Grid) -> None:
        # The shape for each tetrimino is a just a list of positions
        # So we loop through them with a step using range()
        for i in range(0,len(self.current_shape),2):
            # Variables for coordinates
            new_x_pos:int = self.x_pos + self.current_shape[i] # X Coord
            new_y_pos:int = self.y_pos + self.current_shape[i+1] # Y Coord

            # Setting the position
            grid.Set_Grid_Value(new_y_pos, new_x_pos, self.type_of_shape) 
    def Draw_On_Grid(self, screen:pygame.Surface, grid:Grid) -> None:
        # The shape for each tetrimino is a just a list of positions
        # So we loop through them with a step using range()
        for i in range(0,len(self.current_shape),2):
            # Variables for coordinates
            new_x_pos:int = self.x_pos + self.current_shape[i] # X Coord
            new_y_pos:int = self.y_pos + self.current_shape[i+1] # Y Coord

            # Setting the position
            grid.Set_Grid_Value(new_y_pos, new_x_pos, self.type_of_shape) 
            grid.Set_Grid_Value(new_y_pos, new_x_pos, 7)

            # Multiply by cellsize
            new_x_pos *= CELLSIZE
            new_y_pos *= CELLSIZE

            # Drawing the rectangle
            rectangle:pygame.Rect = pygame.Rect(new_x_pos, new_y_pos, CELLSIZE, CELLSIZE)
            pygame.draw.rect(screen, colors[self.type_of_shape], rectangle)
    def CollisionWall(self, grid:Grid) -> bool:
        # loop through each part of the tetrimino
        # If it is on a border return true
        for i in range(0,len(self.current_shape), 2):
            # Variables for coordinates
            new_x_pos:int = self.x_pos + self.current_shape[i] # X Coord
            new_y_pos:int = self.y_pos + self.current_shape[i+1] + 1 # Y Coord

            # if it contiains a border
            if grid.Is_Grid_Value(new_y_pos, new_x_pos, 8):
                return True

        return False # No Collision
    def CollisionAnything(self, grid:Grid) -> bool:
        # loop through each part of the tetrimino
        # If it is on a border return true
        for i in range(0,len(self.current_shape), 2):
            # Variables for coordinates
            new_x_pos:int = self.x_pos + self.current_shape[i] # X Coord
            new_y_pos:int = self.y_pos + self.current_shape[i+1] + 1 # Y Coord

            # if it contiains a border
            if grid.Is_Grid_Value_Range(new_y_pos, new_x_pos, 0, 6):
                return True

        return False