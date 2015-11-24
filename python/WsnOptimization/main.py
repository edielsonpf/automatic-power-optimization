'''
Created on Nov 20, 2015

@author: Edielson
'''
from algorithms.mst import MST
from network.wsn import WSN
import math, logging
from gurobipy import *
from optimizer.flow import Flow
from optimizer.backup import Backup


if __name__ == '__main__':
    pass

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
print('Reduction: ' + str((1-(newTotal/total))*100)+'%\n')


##################################################
#creating data for backup model 

nodes = [1, 2, 3, 4, 5]

links, capacity = multidict({
  (1, 2):   1,
  (1, 3):   1,
  (1, 4):   1,
  (1, 5):   1,
  (2, 1):   1,
  (2, 3):   1,
  (2, 4):   1,
  (2, 5):   1,
  (3, 1):   1,
  (3, 2):   1,
  (3, 4):   1,
  (3, 5):   1,
  (4, 1):   1,
  (4, 2):   1,
  (4, 3):   1,
  (4, 5):   1,
  (5, 1):   1,
  (5, 2):   1,
  (5, 3):   1,
  (5, 4):   1})

links = tuplelist(links)

cost = {
  (1, 2):   1,
  (1, 3):   1,
  (1, 4):   1,
  (1, 5):   1,
  (2, 1):   1,
  (2, 3):   1,
  (2, 4):   1,
  (2, 5):   1,
  (3, 1):   1,
  (3, 2):   1,
  (3, 4):   1,
  (3, 5):   1,
  (4, 1):   1,
  (4, 2):   1,
  (4, 3):   1,
  (4, 5):   1,
  (5, 1):   1,
  (5, 2):   1,
  (5, 3):   1,
  (5, 4):   1}


p = 0.025
invstd = 2.326347874
me = p
var = p*(1-p)
  
mean = {
  (1, 2):   me,
  (1, 3):   me,
  (1, 4):   me,
  (1, 5):   me,
  (2, 1):   me,
  (2, 3):   me,
  (2, 4):   me,
  (2, 5):   me,
  (3, 1):   me,
  (3, 2):   me,
  (3, 4):   me,
  (3, 5):   me,
  (4, 1):   me,
  (4, 2):   me,
  (4, 3):   me,
  (4, 5):   me,
  (5, 1):   me,
  (5, 2):   me,
  (5, 3):   me,
  (5, 4):   me}

variance = {
  (1, 2):   var,
  (1, 3):   var,
  (1, 4):   var,
  (1, 5):   var,
  (2, 1):   var,
  (2, 3):   var,
  (2, 4):   var,
  (2, 5):   var,
  (3, 1):   var,
  (3, 2):   var,
  (3, 4):   var,
  (3, 5):   var,
  (4, 1):   var,
  (4, 2):   var,
  (4, 3):   var,
  (4, 5):   var,
  (5, 1):   var,
  (5, 2):   var,
  (5, 3):   var,
  (5, 4):   var}
        
myBackup = Backup(nodes,links,capacity,cost,mean,variance,invstd)
myBackup.optimize()


