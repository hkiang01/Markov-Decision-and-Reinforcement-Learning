from Grid import * 
import sys
	
for iterations in xrange(10, 11):
	my_grid = Grid("grid.txt", iterations)
	for col in xrange(0,my_grid.cols):
		for row in xrange(0,my_grid.rows):
			my_grid.calcIntendedDirection(row, col)
	my_grid.printGrid()
	my_grid.printIntendedDirections()
	my_grid.printUtilities()


my_grid.setCurrentPosition(3,2) #start position
my_grid.printGrid()

for k in xrange(0, 10000): #number of trials
	for i in xrange(my_grid.rows-1, -1, -1):
		for j in xrange(my_grid.cols-1, -1, -1):
			my_grid.TDLearning(i, j)
			#my_grid.printUtilities()
			#my_grid.printVisitedCount()			
			#my_grid.printQUtilities()

# for i in xrange(0, 10): #number of moves
# 	my_grid.TDLearning(my_grid.currRow, my_grid.currCol)
# 	nextMove = my_grid.grid[my_grid.currRow][my_grid.currCol].qIntendedDirection
# 	my_grid.move(nextMove)
# 	my_grid.printUtilities()
# 	my_grid.printVisitedCount()			
# 	my_grid.printQUtilities()
# 	my_grid.printRMSErrors()

for i in xrange(0,my_grid.rows):
	for j in xrange(0, my_grid.cols):
		my_grid.grid[i][j].calcRMSError()

my_grid.printUtilities()
my_grid.printVisitedCount()			
my_grid.printQUtilities()
my_grid.printRMSErrors()
