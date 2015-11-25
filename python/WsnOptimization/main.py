'''
Created on Nov 20, 2015

@author: Edielson
'''
from algorithms.mst import MST
from network.wsn import WSN
import logging
from gurobipy import tuplelist
from optimizer.backup import Backup
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

p = 0.025
invstd = 2.326347874


# Defining a transmission power vector with maximum power level for all nodes

powerVector = [maxPower for x in range(numNodes)]
total = sum(powerVector)
print('Initial total power: ' + str(total)+'\n')

# Creating scenario  
Network = WSN(powerVector,numNodes,frequency,threshold,area,minPower,logLevel)
Graph = Network.generateScenario()

Scenario = []
Scenario = Network.getScenario()

# Create a trace
# trace = go.Scatter(
#     x = Scenario[],
#     y = random_y,
#     mode = 'markers'
# )
# 
# data = [trace]
# 
# # or plot with: 
# plot_url = py.plot(data, filename='basic-line')
print('Optimizing power direct...\n')
powerVector = Network.optimize(Graph)
totalI = sum(powerVector)
print('Total power [Phase I]: ' + str(totalI))
print('Reduction [Phase I]: ' + str((1-(totalI/total))*100)+'%\n')
#===============================================================================
print('Optimizing power with backup links...\n')

links = Network.getLinks(Graph)
links = tuplelist(links)

#generating nodes list
nodes = []
for i in range(numNodes):
    nodes.append(i)


capacity={}
cost = {}
mean={}
variance={}
for i,j in links:
    #generating capacity list
    capacity[i,j] = 1
    #generating cost list
    cost[i,j] = Graph[i][j]
    #cost[i,j] = 1
    #generating mean list
    mean[i,j] = p
    variance[i,j]=p*(1-p)

#print(capacity)
#print(cost)
#print(mean)
#print(variance)

##################################################
#creating data for backup model 

#nodes = [1, 2, 3, 4, 5]

# links, capacity = multidict({
#   (1, 2):   1,
#   (1, 3):   1,
#   (1, 4):   1,
#   (1, 5):   1,
#   (2, 1):   1,
#   (2, 3):   1,
#   (2, 4):   1,
#   (2, 5):   1,
#   (3, 1):   1,
#   (3, 2):   1,
#   (3, 4):   1,
#   (3, 5):   1,
#   (4, 1):   1,
#   (4, 2):   1,
#   (4, 3):   1,
#   (4, 5):   1,
#   (5, 1):   1,
#   (5, 2):   1,
#   (5, 3):   1,
#   (5, 4):   1})


# links = tuplelist(links)

# cost = {
#   (1, 2):   1,
#   (1, 3):   1,
#   (1, 4):   1,
#   (1, 5):   1,
#   (2, 1):   1,
#   (2, 3):   1,
#   (2, 4):   1,
#   (2, 5):   1,
#   (3, 1):   1,
#   (3, 2):   1,
#   (3, 4):   1,
#   (3, 5):   1,
#   (4, 1):   1,
#   (4, 2):   1,
#   (4, 3):   1,
#   (4, 5):   1,
#   (5, 1):   1,
#   (5, 2):   1,
#   (5, 3):   1,
#   (5, 4):   1}


# p = 0.025
# invstd = 2.326347874
# me = p
# var = p*(1-p)
  
# mean = {
#   (1, 2):   me,
#   (1, 3):   me,
#   (1, 4):   me,
#   (1, 5):   me,
#   (2, 1):   me,
#   (2, 3):   me,
#   (2, 4):   me,
#   (2, 5):   me,
#   (3, 1):   me,
#   (3, 2):   me,
#   (3, 4):   me,
#   (3, 5):   me,
#   (4, 1):   me,
#   (4, 2):   me,
#   (4, 3):   me,
#   (4, 5):   me,
#   (5, 1):   me,
#   (5, 2):   me,
#   (5, 3):   me,
#   (5, 4):   me}
# 
# variance = {
#   (1, 2):   var,
#   (1, 3):   var,
#   (1, 4):   var,
#   (1, 5):   var,
#   (2, 1):   var,
#   (2, 3):   var,
#   (2, 4):   var,
#   (2, 5):   var,
#   (3, 1):   var,
#   (3, 2):   var,
#   (3, 4):   var,
#   (3, 5):   var,
#   (4, 1):   var,
#   (4, 2):   var,
#   (4, 3):   var,
#   (4, 5):   var,
#   (5, 1):   var,
#   (5, 2):   var,
#   (5, 3):   var,
#   (5, 4):   var}
        
myBackup = Backup(nodes,links,capacity,cost,mean,variance,invstd)
solution = myBackup.optimize()

#print(Graph)
NewGraph = [[unconnected for i in range(numNodes)] for i in range(numNodes)]
# for i in range(len(Graph)):
#     for j in range(len(Graph)):
#         NewGraph[i][j]=Graph[i][j]

#penalizes the links chosen to be backup links
for i,j in links:
    #print(solution[i,j])
    if solution[i,j] > 0:
        #NewGraph[i][j]=Graph[i][j]+10
        #NewGraph[j][i]=Graph[j][i]+10
        NewGraph[i][j]=Graph[i][j]
        #NewGraph[j][i]=Graph[j][i]
#print(NewGraph)

powerVector = Network.optimize(NewGraph)
TotalII = sum(powerVector)
print('Total power [Phase II]: '+ str(TotalII))
print('Reduction [Phase II]: ' + str((1-(TotalII/total))*100)+'%\n')
#====================================================================
print('Optimizing the new graph after MST...\n')
#Graph = [[unconnected, 2, unconnected, 6, unconnected], [2, unconnected, 3, 8, 5], [unconnected, 3, unconnected, unconnected, 7],[6, 8, unconnected, unconnected, 9], [unconnected, 5, 7, 9, unconnected]]
#Graph = [[100000, 1.6886794115948998, 2.3122223520756173, 5.296711537472404, 3.5272263704139903], [1.6886794115948998, 100000, 2.91118563715952, 4.489562628012171, 3.2441779819626384], [2.3122223520756173, 2.91118563715952, 100000, 3.789229517634896, 100000], [5.296711537472404, 4.489562628012171, 3.789229517634896, 100000, 100000], [3.5272263704139903, 3.2441779819626384, 100000, 100000, 100000]]
#Graph = [[100000, 2.776731497489389, 5.5709380662188925, 100000, 3.3655359288501994], [2.776731497489389, 100000, 3.2242450750420453, 100000, 4.131843423863429], [5.5709380662188925, 3.2242450750420453, 100000, 100000, 100000], [100000, 100000, 100000, 100000, 100000], [3.3655359288501994, 4.131843423863429, 100000, 100000, 100000]]

#print (str(Graph))
print('Finding the minimum spanning tree...\n')
myMST = MST(Graph,unconnected,logLevel)
MSTGraph1 = myMST.prim()
myMST.printMST()

#print (str(NewGraph))

# must keep connection in both directions
for i in range(len(MSTGraph1)):
    for j in range(len(MSTGraph1)):
        if MSTGraph1[i][j] < unconnected:
            MSTGraph1[j][i] = Graph[j][i]


#print (str(MSTGraph1))
powerVector = Network.optimize(MSTGraph1)
TotalIII = sum(powerVector)
print('Total power: '+ str(TotalIII))
print('Reduction: ' + str((1-(TotalIII/total))*100)+'%\n')

############################################################

#print('Finding the minimum spanning tree...\n')
#myMST = MST(NewGraph,unconnected,logLevel)
#MSTGraph2 = myMST.prim()
#myMST.printMST()

#print (str(NewGraph))

# must keep connection in both directions
#for i in range(len(MSTGraph2)):
#    for j in range(len(MSTGraph2)):
#        if MSTGraph2[i][j] < unconnected:
#            MSTGraph2[j][i] = NewGraph[j][i]

#removes penalties applied to the links chosen to be backup links
# for i,j in links:
#     #print(solution[i,j])
#     if solution[i,j] > 0:
#         MSTGraph2[i][j]=NewGraph[i][j]-10
#         MSTGraph2[j][i]=NewGraph[j][i]-10


