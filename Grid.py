
discountFactor = 0.99
rewardFunction = -0.04

#a C-like struct for a cell in the maze
#resource: http://stackoverflow.com/questions/35988/c-like-structures-in-python
class Cell(object):
	def __init__(self, in_value, in_wall, in_start):
		self.value = in_value #a float
		self.utility = 0 #calculated with Bellman equation
		self.wall = in_wall #a bool
		self.start = in_start #a bool
		self.intendedDirection = -1 #0 up, 1 right, 2 down, 3 left, -1 unassigned
		#how many times we have taken a certain action from this cell (state)
		#see "Incorporating exploration" (slide 12) in lecture 17 (Reinforcement Learning)
		self.actionUp = 0
		self.actionRight = 0
		self.actionDown = 0
		self.actionLeft = 0
		self.currPos = False
		
	#getters
	def getValue(self):
		return self.value
		
	def getUtility(self):
		return self.utility
		
	def isWall(self):
		return self.wall
		
	def isStart(self):
		return self.start
	
	def isCurrentPosition(self):
		return self.currPos
	
	#setters
	def setValue(self, in_value):
		self.value = in_value
		
	def setUtility(self, in_utility):
		self.utility = in_utility

class Grid(object):
	grid = [] # a 2d list of cells
	rows = 0
	cols = 0
	numTotalIterations = 10
	def parseGrid(self, filename):
		print "parsing grid"
		f = open(filename, "r")
		lines = f.readlines()
		f.close()
		curr_grid = []
		self.cols = len(lines[0])-1 #-1 for newline character
		self.rows = len(lines)
		print "There are", self.rows, "rows and", self.cols, "columns"
		for line in lines:
			curr_line = []
			for c in line:
				print c, #print in format of grid.txt
				if(c==' '):
					#print "appending blank cell"
					curr_line.append(Cell(0.0, False, False))
				elif(c=='W'):
					#print "appending wall"
					curr_line.append(Cell(0.0, True, False))
				elif(c=='+'):
					#print "appending +1"
					curr_line.append(Cell(1.0, False, False))
				elif(c=='-'):
					#print "appending -1"
					curr_line.append(Cell(-1.0, False, False))
				elif(c=='S'):
					#print "appending start"
					curr_line.append(Cell(0.0, False, True))
				elif(c=='\n'):
					continue #realines returns '\n' terminated strings
				else:
					#this shouldn't happen
					print "Error: Invalid Cell"
			curr_grid.append(curr_line)
		print "grid parsed"
		self.grid = curr_grid
		return curr_grid
				
	def printGrid(self):
		print "printing grid..."
		for row in self.grid:
			for col in row:
				if(col.isWall()==True):
					print "W\t",
				elif(col.isStart()==True):
					print "S\t",
				elif(col.isCurrentPosition()==True):
					print "*\t",
				else:
					print col.getValue(),
					print "\t",
			print "\n",
		print "grid printed"
	
	def calcIntendedDirection(self, row, col):
		
		def calcIntendedDirectionHelper(self, row, col, numIterations, utility):
			#out of bounds. same as wall
			if(row < 0 or col < 0 or row > self.rows-1 or col > self.cols-1):
				utility += rewardFunction
				return utility
			#wall, same as out of bounds
			if(self.grid[row][col].isWall==True):
				utility += rewardFunction
				return utility
			#last iteration
			if(numIterations<=0):
				return utility
			if(self.grid[row][col].value!=0):
				utility += self.grid[row][col].value
			else:
				utility += rewardFunction
			numIterations -= 1
			uUtil = calcIntendedDirectionHelper(self, row-1, col, numIterations, utility)
			rUtil = calcIntendedDirectionHelper(self, row, col+1, numIterations, utility)
			dUtil = calcIntendedDirectionHelper(self, row+1, col, numIterations, utility)
			lUtil = calcIntendedDirectionHelper(self, row, col-1, numIterations, utility)
			return max(uUtil, rUtil, dUtil, lUtil)
			
	
		uUtil = calcIntendedDirectionHelper(self, row-1, col, self.numTotalIterations, 0)
		rUtil = calcIntendedDirectionHelper(self, row, col+1, self.numTotalIterations, 0)
		dUtil = calcIntendedDirectionHelper(self, row+1, col, self.numTotalIterations, 0)
		lUtil = calcIntendedDirectionHelper(self, row, col-1, self.numTotalIterations, 0)
		
		temp = max(uUtil, rUtil, dUtil, lUtil)
		
		if(uUtil==temp):
			self.grid[row][col].intendedDirection = 0
		elif(rUtil==temp):
			self.grid[row][col].intendedDirection = 1
		elif(dUtil==temp):
			self.grid[row][col].intendedDirection = 2
		else:
			self.grid[row][col].intendedDirection = 3
			
		self.grid[row][col].utility = temp
		print "(", col, ",", row, "): ", temp#self.grid[row][col].intendedDirection
	
	def printIntendedDirections(self):
		print "printing directions..."
		for row in self.grid:
			for col in row:
				if(col.isWall()==True):
					print "W\t",
				else:
					if(col.intendedDirection==0):
						print "^\t",
					elif(col.intendedDirection==1):
						print ">\t",
					elif(col.intendedDirection==2):
						print "v\t",
					else:
						print "<\t",
			print "\n",
		print "grid printed"
	
	def printUtilities(self):
		for row in self.grid:
			for col in row:
					print col.utility, "\t",
			print "\n",
	
	#reset grid utitlies 
	def resetGridUtilities(self):
		for row in self.grid:
			for col in row:
				col.utility = 0
	
	def setCurrentPosition(self, in_row, in_col):
		#flush out all old current positions
		for row in self.grid:
			for col in row:
				col.currPos = False
		
		#update the grid with a new current position
		self.grid[in_row][in_col].currPos = True
	
	def __init__(self, filename_grid, num_iterations):
		self.grid = self.parseGrid(filename_grid)
		self.numTotalIterations = num_iterations

