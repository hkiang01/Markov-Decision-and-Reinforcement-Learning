from Grid import * 
import sys



#row_counter = 0
#for row in my_grid.grid:
#	col_counter = 0
#	for col in row:
#		my_grid.calcIntendedDirection(row_counter, col_counter)
#		col_counter += 1
#	row_counter += 1
	
for iterations in xrange(10, 0, -5):
	my_grid = Grid("grid.txt", iterations)
	for col in xrange(0,my_grid.cols):
		for row in xrange(0,my_grid.rows):
			my_grid.calcIntendedDirection(row, col)
	my_grid.printGrid()
	my_grid.printIntendedDirections()

