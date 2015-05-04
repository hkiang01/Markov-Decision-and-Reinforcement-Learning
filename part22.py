#part2.2
from __future__ import division
from operator import add,sub
import numpy as np
import copy,sys


def parse(filename):
    f = open(filename, "r")
    content = f.readlines()
    f.close()
    labelList = []
    retList = []
    for line in content:
        curr_dict = {}
	elements = line.rsplit(' ')
	curr_label = int(elements[0])
	labelList.append(curr_label)

	#skip the first element
	#http://stackoverflow.com/questions/10079216/skip-first-entry-in-for-loop-in-python
	iterElements = iter(elements) #skip the first element
	next(iterElements) #the first element contains the label
	for elem in iterElements:
	    temp = elem.rsplit(':')
	    key = temp[0]
	    value = int(temp[1])
	    curr_dict[key] = value #add entry into dictionary
	retList.append(curr_dict)
    return labelList,retList
    
def createDictionary(inputLabels,inputDict):
    counter = 0
    retList = [{},{},{},{},{},{},{},{}]
    for dictionary in inputDict:
	category = inputLabels[counter]
	for word in dictionary:
	   key = word #the word
	   value = dictionary.get(key) #the frequency
	   value += retList[category].get(key, 0) #increase the value (frequency) by the existing entry's value, default is 0 if none is found
	   retList[category][key] = value #update the entry
        counter += 1
    return retList

trainLabels, trainDict = copy.deepcopy(parse("8category.training.txt"))
Dictionary = copy.deepcopy(createDictionary(trainLabels, trainDict))
#Dictionary holds 8 dictionaries - one for each category

iterations = int(sys.argv[1])
random = sys.argv[2]

W = []
for i in Dictionary:
    curW = []
    for j in range(len(i)):
        if(random == 'r'):
            curW.append(np.random(0,1))
        elif(random == 'z'):
            curW.append(0)
        else:
            print "input error: use 'r' or 'z' to indicate weight init"
            return
    W.append(curW)












