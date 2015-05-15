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

#1900 vectors
def createTrainingVectors(inputDict):
    vectorList = []
    for dictionary in inputDict:
        currList = []
        for entry in sorted(dictionary):
            #print entry, dictionary[entry]
            currList.append(dictionary[entry])
        vectorList.append(currList)
    return vectorList


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


#returns a list of vectors corresponding to each test document
def parseTest(filename, catDict):

    #LABELS
    labelList = []
    f = open(filename, "r")
    content = f.readlines()
    f.close()

    for line in content:
        curr_dict = {}
        elements = line.rsplit(' ')
        curr_label = int(elements[0])
        labelList.append(curr_label)
    #END LABELS

    #VECTORS
    vectorList = []

    for line in content: #line refers to a document
        candidateVectors = []
        for category in xrange(len(catDict)):
            currVector = []

            candidateVectors.append(currVector)

        bestCat = np.argmax(candidateVectors)
        
        

    #END VECTORS


    return labelList, vectorList



trainLabels, trainDict = parse("8category.training.txt")
#1900 training vectors
trainList = createTrainingVectors(trainDict)
print len(trainList)
Dictionary = createDictionary(trainLabels, trainDict)
#Dictionary holds 8 dictionaries - one for each category
testLabels, testList = parseTest("8category.testing.txt", Dictionary) 
#testLabels = parseTest("8category.testing.txt")
#print testLabels


iterations = int(sys.argv[1])
random = sys.argv[2]

print Dictionary

sys.exit(0)



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
            #return
    W.append(curW)


result = []
f = open('output'+random,'w')
for i in range(iterations):
    trainCorrect = 0
    alpha = 1000/(1000+i)
    for index,x in enumerate(trainList): #enumerate through the list of training vectors
        cprime = np.argmax(np.dot(W,x)) # c' = argmax(8 element list of probabilities based on weights)
        c = trainLabels[index]          # c = actual label from trainlabels
        if(cprime != c):                #increase weight for correct class, and reduce weight for incorrect
            W[c] = map(add,W[c],[k*alpha for k in x])             #wc <- wc + ax
            W[cprime] = map(sub, W[cprime],[k*alpha for k in x])  #wc' <- wc' - ax
        else:
            trainCorrect += 1
    accuracy = trainCorrect/sample_size
    result.append(accuracy)
    if(i % 10 == 0):
        print "reached ",(accuracy*100),"% accuracy at epoch ",i
    f.write("reached "+str(accuracy*100)+"% accuracy at epoch "+str(i))
    if(accuracy == 1):
        break



confusion = [[0 for i in range(8)] for j in range(8)]
testCorrect = 0

for index,x in enumerate(testList):
    cprime = np.argmax(np.dot(W,x)) # c' = argmax(8 element list of probabilities based on weights)
    c = testLabels[index]          # c = actual label from testlabels
    confusion[c][cprime] += 1
    if(c == cprime):
        testCorrect +=1
testAccuracy = testCorrect/len(testLabels)

for i in range(8):
    total = np.sum(confusion[i])
    for j in range(8):
        confusion[i][j] = confusion[i][j]/total


f.write(str(confusion))
f.write('\n') # python will convert \n to os.linesep
f.write(str(testAccuracy))
f.close()

plt.plot(result)
plt.savefig("plot"+random)
