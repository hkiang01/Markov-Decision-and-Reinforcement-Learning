import numpy as np #importing numpy (not used at time of writing)
import scipy as sp #importing scipy (not used at time of writing)


# GLOBAL 
NUM_CLASSES = 10
NUM_ROWS = 28
NUM_COLS = 28

#Class Digit
class Digit(object):

    properClass = 0
    V = 2

    #define class to store the digit
    def __init__(self, numFeatures=2): #default constructor
        self.number = []
        self.features = []
        self.V = numFeatures
    
    #translate parsed file to 0's and 1's
    def processFeatures(self):
    	ret_list = []
    	for s in self.number: #s is a string
    		curr_line = []
    		for c in s:
    			if c=='#':
    				curr_line.append(1.0)
    			elif c=='+':
    				if (self.V==2):
    					curr_line.append(1.0)
    				else:
    					curr_line.append(0.8)
    			else:
    				curr_line.append(0.0)
    		ret_list.append(curr_line)
    	self.features = ret_list
    
    # reference: http://www.kosbie.net/cmu/fall-11/15-112/handouts/notes-2d-lists.html
    def printNumber(self): #digit is implicit argument
        if (self.number==[]): # null check for empty list
        	print [] # prevents crashing on accessing number[0]
        	return
        for row in xrange(NUM_ROWS): #xrange returns xrange object
        # xrange, see: https://wiki.python.org/moin/ForLoop
        # xrange is more efficient with memory than range
           	curr_line = ""
           	for col in xrange(NUM_COLS): 
          		curr_line += self.number[row][col]
           	print curr_line
           	

    def printFeatures(self):
    	for row in xrange(NUM_ROWS):
    		curr_line = ""
    		for col in xrange(NUM_COLS):
    			curr_line += (str(self.features[row][col]))
    		print curr_line
    
    def calcSimilarityHeuristic(self, a_digit):
    	heuristic = 0
    	for row in xrange(0, NUM_ROWS):
    		for col in xrange(0, NUM_COLS):
    			if(self.features[row][col] == a_digit.features[row][col] >= 0.5):
    				heuristic += 1
    	return heuristic

    def setProperClass(self, value):
        self.properClass = value

    def getProperClass(self):
        return self.properClass

### NOTES ###

# DIVISION
# / #float
# // #floor

# FOR LOOPS
# for row in xrange(0, NUM_ROWS)
# same as
# for row in xrange(NUM_ROWS)
# lower bound inclusive, assumed 0
# upper bound exclusive, must be defined
