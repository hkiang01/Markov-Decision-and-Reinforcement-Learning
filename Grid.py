import math

discountFactor = 0.99
rewardFunction = -0.04
intendedDirectionLikelihood = 0.8
rightAngleLikelihood = 0.1
conversionThreshold = 0.03271627750388923

#a C-like struct for a cell in the maze
#resource: http://stackoverflow.com/questions/35988/c-like-structures-in-python
class Cell(object):
	def __init__(self, in_value, in_wall, in_start):
		self.value = in_value #a float
		self.utility = 0 #calculated with Bellman equation
		self.qutility = [float(in_value)] #for TD learning
		self.wall = in_wall #a bool
		self.start = in_start #a bool
		self.intendedDirection = -1 #0 up, 1 right, 2 down, 3 left, -1 unassigned
		self.probUp = 0.0
		self.probRight = 0.0
		self.probDown = 0.0
		self.probLeft = 0.0
		#how many times we have taken a certain action from this cell (state)
		#see "Incorporating exploration" (slide 12) in lecture 17 (Reinforcement Learning)
		self.actions = [0,0,0,0] #number of times gone up, right, down, left
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
	currRow = -1 #initially not in the maze
	currCol = -1
	#t = 0
	#alpha = 60.0/59
	Ne = 5
	RPlus = 1 #most optimal estimate DOUBLE CHECK

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
			uUtil = discountFactor*calcIntendedDirectionHelper(self, row-1, col, numIterations, utility)
			rUtil = discountFactor*calcIntendedDirectionHelper(self, row, col+1, numIterations, utility)
			dUtil = discountFactor*calcIntendedDirectionHelper(self, row+1, col, numIterations, utility)
			lUtil = discountFactor*calcIntendedDirectionHelper(self, row, col-1, numIterations, utility)

			temp = max(uUtil, rUtil, dUtil, lUtil)
			if(temp <= conversionThreshold):
				return temp #no contribution if below threshold
			else:
				return temp
			
	
		uUtil = calcIntendedDirectionHelper(self, row-1, col, self.numTotalIterations, 0)
		rUtil = calcIntendedDirectionHelper(self, row, col+1, self.numTotalIterations, 0)
		dUtil = calcIntendedDirectionHelper(self, row+1, col, self.numTotalIterations, 0)
		lUtil = calcIntendedDirectionHelper(self, row, col-1, self.numTotalIterations, 0)
		
		temp = max(uUtil, rUtil, dUtil, lUtil)
		
		if(uUtil==temp):#up
			self.grid[row][col].intendedDirection = 0
			self.grid[row][col].probUp = intendedDirectionLikelihood
			self.grid[row][col].probRight = rightAngleLikelihood
			self.grid[row][col].probDown = 0.0
			self.grid[row][col].probLeft = rightAngleLikelihood
		elif(rUtil==temp):#right
			self.grid[row][col].intendedDirection = 1
			self.grid[row][col].probUp = rightAngleLikelihood
			self.grid[row][col].probRight = intendedDirectionLikelihood
			self.grid[row][col].probDown = rightAngleLikelihood
			self.grid[row][col].probLeft = 0.0
		elif(dUtil==temp):#down
			self.grid[row][col].intendedDirection = 2
			self.grid[row][col].probUp = 0.0
			self.grid[row][col].probRight = rightAngleLikelihood
			self.grid[row][col].probDown = intendedDirectionLikelihood
			self.grid[row][col].probLeft = rightAngleLikelihood
		else:#left
			self.grid[row][col].intendedDirection = 3
			self.grid[row][col].probUp = rightAngleLikelihood
			self.grid[row][col].probRight = 0.0
			self.grid[row][col].probDown = rightAngleLikelihood
			self.grid[row][col].probLeft = intendedDirectionLikelihood
			
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
		if(in_row < 0 or in_row > self.rows-1 or in_col < 0 or in_col > self.cols-1):
			print "out of bounds in setCurrentPosition"
		
		print "Moving to(", in_row, ",", in_col, ")"
		#update the grid with a new current position
		self.grid[self.currRow][self.currCol].currPos = False
		self.grid[in_row][in_col].currPos = True
		self.currRow = in_row
		self.currCol = in_col

	def TDLearning(self, in_row, in_col):

		def QSA(in_row, in_col, candidate_move):
			print "QSA...",

			if(candidate_move==0):
				print "candidate_move=up"
			elif(candidate_move==1):
				print "candidate_move=right"
			elif(candidate_move==2):
				print "candidate_move=down"
			elif(candidate_move==3):
				print "candidate_move=left"
			else:
				print "Error: invalid candidate_move for QSA"

			currCell = self.grid[in_row][in_col]
			col = int(in_col+round(math.sin(math.radians(candidate_move*90))))
			row = int(in_row+round(math.sin(math.radians(candidate_move*90-90))))

			if(row<0 or row > self.rows-1 or col<0 or col > self.cols-1):
				print "out of bounds"
				if(currCell.value!=0):
					return currCell.value
				return rewardFunction

			candidateCell=self.grid[row][col]
			#candidate cell is wall
			if(candidateCell.isWall()==True):
				print "wall",
				#look at the current cell
				if(currCell.value!=0):
					print "returning value"
					return currCell.value
				else:
					print "returning reward function"
					return rewardFunction
			#can move to candidate cell
			print "valid move",
			if(candidateCell.value!=0.0):
				print "returning value"
				return candidateCell.value
			else:
				print "returning reward function"
				return rewardFunction

		def QSAP(in_row, in_col, candidate_move):
			currCell = self.grid[in_row][in_col]
			col = int(in_col+round(math.sin(math.radians(candidate_move*90))))
			row = int(in_row+round(math.sin(math.radians(candidate_move*90-90))))
			if(row<0 or row > self.rows-1 or col<0 or col > self.cols-1):
				if(currCell.value!=0):
					return currCell.value
				else:
					return rewardFunction
			
			upVal = QSA(row, col, 0)
			print "QSAP upVal", upVal
			rightVal = QSA(row, col, 1)
			print "QSAP rightVal", rightVal
			downVal = QSA(row, col, 2)
			print "QSAP downVal", downVal
			leftVal = QSA(row, col, 3)
			print "QSAP leftVal", leftVal
			return max(upVal, rightVal, downVal, leftVal)
		
		def getAction(in_row, in_col):
			def fun(in_row, in_col, candidate_action):
				currCell = self.grid[in_row][in_col]
				if(currCell.actions[candidate_action] > self.Ne):
					print "fun condition met, returning reward function"
					return self.RPlus
				else:
					print "fun condition not met, returning  QSAP"
					return QSAP(in_row, in_col, candidate_action)

			print "getting action..."
			candidateActions = [0.0,0.0,0.0,0.0]
			candidateActions[0] = fun(in_row, in_col, 0) #up call
			print "getAction up value", candidateActions[0]
			candidateActions[1] = fun(in_row, in_col, 1) #right call
			print "getAction right value", candidateActions[1]
			candidateActions[2] = fun(in_row, in_col, 2) #down call
			print "getAction down value", candidateActions[2]
			candidateActions[3] = fun(in_row, in_col, 3) #left call
			print "getAction left value", candidateActions[3]
			temp = candidateActions.index(max(candidateActions))
			self.grid[in_row][in_col].actions[temp] += 1 #update n for the respective action in a cell
			return temp

		def TDHelper(qutil, in_row, in_col): #alpha is floating point number

			#recursive calls to get QSPAP
			t = len(self.grid[in_row][in_col].qutility) #increments t
			print "TDHelper t (timestep)", t
			alpha = float(60)/(59+t)
			print "TDHelper alpha", alpha
			retVal = qutil
			print "TDHelper qutil", qutil
			upVal = QSAP(in_row, in_col, 0)
			print "TDHelper upval", upVal
			rightVal = QSAP(in_row, in_col, 1)
			print "TDHelper rightval", rightVal
			downVal = QSAP(in_row, in_col, 2)
			print "TDHelper downVal", downVal
			leftVal = QSAP(in_row, in_col, 3)
			print "TDHelper leftVal", leftVal
			QSPAP = max(upVal, rightVal, downVal, upVal) #QSPAP = most optimal QSAP
			retVal += float(alpha)*(rewardFunction + discountFactor*QSPAP-qutil)
			print "TDHelper retval", retVal
			return retVal

		print "TDLearning called on [", in_row, ",", in_col, "]"
		action = getAction(in_row, in_col) #get the action
		print "TDLearning action", action
		print "\n"
		currCell = self.grid[in_row][in_col]
		currCell.qutility.append(TDHelper(currCell.qutility[-1], in_row, in_col)) #indexed by timestamp
		#print "action:", action

	def __init__(self, filename_grid, num_iterations):
		self.grid = self.parseGrid(filename_grid)
		self.numTotalIterations = num_iterations

