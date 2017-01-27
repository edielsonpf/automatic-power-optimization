'''
Created on Nov 20, 2015

@author: Edielson
'''
import random, math
from algorithms.mst import MST
from network.wsn import WSN
import logging

#from optimizer.backup import Backup
#from networkx.classes.graph import Graph

#import plotly.plotly as py
#import plotly.graph_objs as go

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

# generate random positions (x,y) for each node
nodes=[[random.uniform(0, math.sqrt(area)) for i in range(numNodes)] for j in range(2)]
       

# Defining a transmission power vector with maximum power level for all nodes
powerVector = [maxPower for x in range(numNodes)]
total = sum(powerVector)
print('Initial total power: ' + str(total)+'\n')

# Creating network object  
Network = WSN(powerVector,numNodes,nodes,frequency,threshold,minPower,logLevel)

Network.plotGraph(position=None)

print('Optimizing power direct...\n')
powerVector = Network.optimizePower()
totalI = sum(powerVector)
print('Total power [Phase I]: ' + str(totalI))
print('Reduction [Phase I]: ' + str((1-(totalI/total))*100)+'%\n')
#====================================================================
print('Optimizing the new graph after MST...\n')
#Graph = [[unconnected, 2, unconnected, 6, unconnected], [2, unconnected, 3, 8, 5], [unconnected, 3, unconnected, unconnected, 7],[6, 8, unconnected, unconnected, 9], [unconnected, 5, 7, 9, unconnected]]
#Graph = [[100000, 1.6886794115948998, 2.3122223520756173, 5.296711537472404, 3.5272263704139903], [1.6886794115948998, 100000, 2.91118563715952, 4.489562628012171, 3.2441779819626384], [2.3122223520756173, 2.91118563715952, 100000, 3.789229517634896, 100000], [5.296711537472404, 4.489562628012171, 3.789229517634896, 100000, 100000], [3.5272263704139903, 3.2441779819626384, 100000, 100000, 100000]]
#Graph = [[100000, 2.776731497489389, 5.5709380662188925, 100000, 3.3655359288501994], [2.776731497489389, 100000, 3.2242450750420453, 100000, 4.131843423863429], [5.5709380662188925, 3.2242450750420453, 100000, 100000, 100000], [100000, 100000, 100000, 100000, 100000], [3.3655359288501994, 4.131843423863429, 100000, 100000, 100000]]

#print (str(Graph))
print('Finding the minimum spanning tree...\n')
Network.optimizeTopology()

powerVector = Network.optimizePower()
TotalIII = sum(powerVector)
print('Total power: '+ str(TotalIII))
print('Reduction: ' + str((1-(TotalIII/total))*100)+'%\n')

Network.plotGraph(position=None)
