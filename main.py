from Grid import * 
import sys

my_grid = Grid("grid.txt")

#row_counter = 0
#for row in my_grid.grid:
#	col_counter = 0
#	for col in row:
#		my_grid.calcIntendedDirection(row_counter, col_counter)
#		col_counter += 1
#	row_counter += 1
	
for col in xrange(0,my_grid.cols):
	for row in xrange(0,my_grid.rows):
		my_grid.calcIntendedDirection(row, col)
		

my_grid.printGrid()


