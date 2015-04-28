from Grid import * 
import sys

my_grid = Grid("grid.txt")
another_grid = Grid("grid2.txt")
my_grid.grid[0][0].setValue(0.5)
my_grid.printGrid()
another_grid.printGrid()
my_grid.calcUtility(0,0,0)

