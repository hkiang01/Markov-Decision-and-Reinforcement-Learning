

#a C-like struct for a square in the maze
#resource: http://stackoverflow.com/questions/35988/c-like-structures-in-python
class Square(object):
	def __init__(self, in_value, in_wall, in_start):
		self.value = in_value #a float
		self.wall = in_wall #a bool
		self.start = in_start #a bool
		
	#getters
	def getValue(self):
		return self.value
		
	def isWall(self):
		return self.wall
		
	def isStart(self):
		return self.start
	
	#setters
	def setValue(self, in_value):
		self.value = in_value

class Grid(object):
	grid = [] # a 2d list of ints 
	
	def parseGrid(self, filename):
		print "parsing grid"
		f = open(filename, "r")
		lines = f.readlines()
		f.close()
		
		curr_grid = []
		for line in lines:
			curr_line = []
			for c in line:
				print c, #print in format of grid.txt
				if(c==' '):
					#print "appending blank square"
					curr_line.append(Square(0.0, False, False))
				elif(c=='W'):
					#print "appending wall"
					curr_line.append(Square(0.0, True, False))
				elif(c=='+'):
					#print "appending +1"
					curr_line.append(Square(1.0, False, False))
				elif(c=='-'):
					#print "appending -1"
					curr_line.append(Square(-1.0, False, False))
				elif(c=='S'):
					#print "appending start"
					curr_line.append(Square(0.0, False, True))
				elif(c=='\n'):
					continue #realines returns '\n' terminated strings
				else:
					#this shouldn't happen
					print "Error: Invalid Square"
			curr_grid.append(curr_line)
		print "grid parsed"
		return curr_grid
				
	def printGrid(self):
		print "printing grid..."
		for row in self.grid:
			for col in row:
				if(col.isWall()==True):
					print "W\t",
				elif(col.isStart()==True):
					print "S\t",
				else:
					print col.getValue(),
					print "\t",
			print "\n",
		print "grid printed"
		
	
	def __init__(self, filename_grid):
		self.grid = self.parseGrid(filename_grid)

