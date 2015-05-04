from Grid import * 
import sys



#row_counter = 0
#for row in my_grid.grid:
#	col_counter = 0
#	for col in row:
#		my_grid.calcIntendedDirection(row_counter, col_counter)
#		col_counter += 1
#	row_counter += 1
	
for iterations in xrange(0, 10):
	my_grid = Grid("grid.txt", iterations)
	for col in xrange(0,my_grid.cols):
		for row in xrange(0,my_grid.rows):
			my_grid.calcIntendedDirection(row, col)
	my_grid.printGrid()
	my_grid.printIntendedDirections()
	my_grid.printUtilities()
	my_grid.setCurrentPosition(3,2)
	my_grid.printGrid()
	for k in xrange(0, 100): #number of trials
		for i in xrange(my_grid.rows-1, -1, -1):
			for j in xrange(my_grid.cols-1, -1, -1):
				#print my_grid.grid[i][j].qutility
				my_grid.TDLearning(i, j)
				#print my_grid.grid[i][j].qutility

	for i in xrange(0,my_grid.rows):
		for j in xrange(0, my_grid.cols):
			my_grid.grid[i][j].calcRMSError()

	my_grid.printUtilities()			
	my_grid.printQUtilities()
	my_grid.printRMSErrors()