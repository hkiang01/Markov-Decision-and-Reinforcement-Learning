from Grid import * 
import sys



#row_counter = 0
#for row in my_grid.grid:
#	col_counter = 0
#	for col in row:
#		my_grid.calcIntendedDirection(row_counter, col_counter)
#		col_counter += 1
#	row_counter += 1
	
for iterations in xrange(5, 0, -5):
	my_grid = Grid("grid.txt", iterations)
	for col in xrange(0,my_grid.cols):
		for row in xrange(0,my_grid.rows):
			my_grid.calcIntendedDirection(row, col)
	my_grid.printGrid()
	my_grid.printIntendedDirections()
	my_grid.printUtilities()
	my_grid.setCurrentPosition(3,2)
	my_grid.printGrid()
	for i in xrange(0,my_grid.rows):
		for j in xrange(0, my_grid.cols):
			for k in xrange(0, 10): #number of trials
				print my_grid.grid[i][j].qutility
				my_grid.TDLearning(i, j)
				print my_grid.grid[i][j].qutility

	for i in xrange(0,my_grid.rows):
		for j in xrange(0, my_grid.cols):
			my_grid.grid[i][j].calcRMSError()
			
	my_grid.printQUtilities()
	my_grid.printRMSErrors()