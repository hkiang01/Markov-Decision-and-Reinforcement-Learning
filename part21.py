#part2.1
from __future__ import division
import copy,sys
import numpy as np
from operator import add,sub
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#parse translates the image data to a (sample_size)x784 element 2D list
def parse(filename, sample_size):

    # f = open(filename, "r")
    # retList = []
    # for i in xrange(0, sample_size):
    #     for j in xrange(0, 28):
    #         currline = f.readline()
    #         currList = []
    #         for c in currline:
    #             if(c=='#' or c=='+'):
    #                 currList.append(1)
    #             elif(c==' '):
    #                 currList.append(0)
    #         retList.append(currList)
    # f.close()
    # return retList

    f = open(filename, "r")
    filestring = f.read()
    f.close()
    retList = []
    for i in range (sample_size):
        curList = []
        start = i*784
        end = start+784
    	curString = filestring[start:end]
        # print "len(curString) =", len(curString)
        for c in curString:
    	    if(c == '#' or c == '+'):
    	        curList.append(1)
    	    elif(c==' '):
    	        curList.append(0)

        while(len(curList)<784): #hacky fix
            curList.append(0)
        
        retList.append(curList)

    print "len(retList) =", len(retList)
    return retList

#begin main

iterations = int(sys.argv[1])
random = sys.argv[2]
sample_size = int(sys.argv[3])#sum(1 for line in open("trainingimages")) // 28


f = open("traininglabels",'r')
trainLabels = map(int,f.readlines())
f.close()

#trainList is a (sample_size)x784 2D list
#each sample is represented by a list of 784 (28x28) digits
#trainList = copy.deepcopy(parse("trainingimages", sample_size))
trainList = parse("trainingimages", sample_size)

f = open("testlabels",'r')
testLabels = map(int,f.readlines())
f.close()
#testList = copy.deepcopy(parse("testimages", len(testLabels)))
testList = parse("testimages", len(testLabels))


for j in xrange(0, 5):
    for i in xrange(28):
        print trainList[j][i*28:(i*28)+28]
    print ""
    
#sys.exit(0)
    
#begin perceptron
W = []
for i in range(10):
    if(random == 'r'): #use random starting values for weights
        curw = np.mat(np.random.uniform(0.00,1.00,784),float) # randomly initialize weights between 0 and 1
        curw = curw.tolist()[0] #w is now a 784 element list of random weights 
    elif(random == 'z'): #use zeros for starting values
        curw = [0 for i in range(784)]
    else:
        print "input error: use 'r' or 'z' to indicate weight init"
    W.append(curw) #W ends up being a 10x784 element 2D list

result = []
f = open('output'+random,'w')
for i in range(iterations):
    trainCorrect = 0
    alpha = 1000/(1000+i)
    for index,x in enumerate(trainList):
        cprime = np.argmax(np.dot(W,x)) # c' = argmax(10 element list of probabilities based on weights)
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



confusion = [[0 for i in range(10)] for j in range(10)]
testCorrect = 0

for index,x in enumerate(testList):
    cprime = np.argmax(np.dot(W,x)) # c' = argmax(10 element list of probabilities based on weights)
    c = testLabels[index]          # c = actual label from testlabels
    confusion[c][cprime] += 1
    if(c == cprime):
        testCorrect +=1
testAccuracy = testCorrect/len(testLabels)

for i in range(10):
    total = np.sum(confusion[i])
    for j in range(10):
        confusion[i][j] = confusion[i][j]/total


f.write(str(confusion))
f.write('\n') # python will convert \n to os.linesep
f.write(str(testAccuracy))
f.close()

plt.plot(result)
plt.savefig("plot"+random)

