'''
Created on Nov 20, 2015

@author: Edielson
'''
from algorithms.mst import MST
from wsn.network import WSN
import math, logging

if __name__ == '__main__':
    pass

# # Method for calculating maximum distance according to the power transmission 
# def caldDistance(power,frequency,level):
#     loss = 32.5 + 20*math.log10(frequency)
#     distance = 10**((maxPower - loss - level)/20)
#     return distance

# Constant definition
logLevel = logging.DEBUG
numNodes = 5
unconnected = 100000
maxPower =  27
minPower = -15
threshold =-80
frequency = 933
area = 50  #square kilometers

# Defining a transmission power vector with maximum power level for all nodes
powerVector = [[maxPower for x in range(numNodes)] for x in range(numNodes)]

#calculating maximum distance for maximum power level
# dmax = caldDistance(maxPower, frequency, minLevel)
# print('Maximum distance: ' + str(dmax) + '\n') 

# Creating scenario  
Network = WSN(powerVector,numNodes,frequency,threshold,area,minPower,logLevel)
myGraph = Network.generateScenario()

powerVector = Network.optimize(myGraph)
total = sum(powerVector)
print('Total power: ' + str(total)+'\n')

#myGraph = [[unconnected, 2, unconnected, 6, unconnected], [2, unconnected, 3, 8, 5], [unconnected, 3, unconnected, unconnected, 7],[6, 8, unconnected, unconnected, 9], [unconnected, 5, 7, 9, unconnected]]
#myGraph = [[100000, 1.6886794115948998, 2.3122223520756173, 5.296711537472404, 3.5272263704139903], [1.6886794115948998, 100000, 2.91118563715952, 4.489562628012171, 3.2441779819626384], [2.3122223520756173, 2.91118563715952, 100000, 3.789229517634896, 100000], [5.296711537472404, 4.489562628012171, 3.789229517634896, 100000, 100000], [3.5272263704139903, 3.2441779819626384, 100000, 100000, 100000]]
#myGraph = [[100000, 2.776731497489389, 5.5709380662188925, 100000, 3.3655359288501994], [2.776731497489389, 100000, 3.2242450750420453, 100000, 4.131843423863429], [5.5709380662188925, 3.2242450750420453, 100000, 100000, 100000], [100000, 100000, 100000, 100000, 100000], [3.3655359288501994, 4.131843423863429, 100000, 100000, 100000]]

#print (str(myGraph))
print('Finding the minimum spanning tree...\n')
myMST = MST(myGraph,unconnected,logLevel)
myNewGraph = myMST.prim()
myMST.printMST()

#print (str(myNewGraph))

# must keep connection in both directions
for i in range(len(myNewGraph)):
    for j in range(len(myNewGraph)):
        if myNewGraph[i][j] < unconnected:
            myNewGraph[j][i] = myGraph[j][i]

print('Optimizing the new graph after MST...\n')
#print (str(myNewGraph))
powerVector = Network.optimize(myNewGraph)
newTotal = sum(powerVector)
print('Total power: '+ str(newTotal)+'\n')
print('Reduction: ' + str((1-(newTotal/total))*100)+'%')
