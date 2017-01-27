'''
Created on Nov 20, 2015

@author: Edielson
'''
import math, logging
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np 
from algorithms.mst import MST

class WSN(object):
    '''
    classdocs
    '''
    __numNodes = 0
    __threshold = 0
    __unconnected = 100000
    __nodes = []
    __power = []
    __graph = []
    __nxGraph = []
       
    def __init__(self,power,num_nodes,nodes,frequency,threshold,min_tx_level,log):
        '''
        Constructor
        '''
        self.__frequency = frequency
        self.__numNodes = num_nodes
        self.__threshold = threshold
        self.__power = power
        self.__minTxLevel = min_tx_level
        self.__configLog(log)
        self.__nodes = nodes    
        self.__mst = MST(log)
        self.__generateGraph()
#         plt.ion() # enables interactive mode
        
    def __configLog(self,log):
        # print a log message to the console.
        logging.basicConfig(format='%(asctime)s %(message)s', level=log)
    
    # Method for calculating maximum distance according to the power transmission 
    def __caldDistance(self,power):
        loss = 32.5 + 20*math.log10(self.__frequency)
        distance = 10**((power - loss - self.__threshold)/20)
        return distance
    
    # Method for calculating maximum distance according to the power transmission 
    def __calcLoss(self,distance):
        return (32.5 + 20*math.log10(self.__frequency) + 20*math.log10(distance))
        
    def __generateGraph(self):
        
        # transforms the indirect graph in directed one
        self.__nxGraph = nx.Graph()
        
        # generated a graph with connection between nodes initially unconnected
        self.__graph = [[self.__unconnected for i in range(self.__numNodes)] for j in range(self.__numNodes)]
        
        ValidConnection = False
        
        for i in range(self.__numNodes):
            for j in range(self.__numNodes):
                if i != j:
                    dist = math.sqrt(((self.__nodes[0][i]-self.__nodes[0][j])**2)+((self.__nodes[1][i]-self.__nodes[1][j])**2))
                    if dist < self.__caldDistance(self.__power[i]):
                        ValidConnection = True
                        self.__graph[i][j] = dist
                        self.__nxGraph.add_edge(i, j) 
        
        if ValidConnection == False:
            logging.warning('The graph is not connected!')
            self.__graph = []
            self.__nxGraph=[]

    def getScenario(self):
        return self.__nodes
    
    def getConnectionGraph(self):
        return self.__graph
    
    def optimizePower(self):
        #optimize each row, finding the farthest node
        for i in range(len(self.__graph)):
            highDistance = 0
            for j in range(len(self.__graph)):
                if (i!=j) & (self.__graph[i][j] < self.__unconnected) & (self.__graph[i][j] > highDistance):
                    highDistance = self.__graph[i][j]  

            #calculate the power of the transmitter for achieving the minimum power level 
            self.__power[i] = self.__threshold+self.__calcLoss(highDistance);
            if self.__power[i] < self.__minTxLevel:
                self.__power[i] = self.__minTxLevel
        
        return self.__power
    
    def optimizeTopology(self):
        self.__graph = self.__mst.prim(self.__graph)
        self.__mst.printMST()
        
        self.__nxGraph.clear()
        
        for i in range(len(self.__graph)):
            for j in range(len(self.__graph)):
                if self.__graph[i][j] < self.__unconnected:
                    self.__nxGraph.add_edge(i, j)
                                
    def getLinks(self):
        
        links = []
        for i in range(len(self.__graph)):
            for j in range(len(self.__graph)):
                if self.__graph[i][j] < self.__unconnected:
                    links.append((i,j))
        return links

    
    def plotGraph(self,position=None):
        """Plot a graph G with specific position.
    
        Parameters
        ----------
        position : nodes position 
        
        Returns
        -------
        
        """
        
        if position == None:
            position=self.__nodes # positions for all nodes
            
            #in this case it is necessary o convert the matrix node to dictionary    
            pos=0
            dict_position={}
            for i in range(self.__numNodes):
                dict_position[pos]=np.array([position[0][i],position[1][i]])
                pos+=1
            
            position = dict_position        
        
        # nodes
        nx.draw_networkx_nodes(self.__nxGraph,position,node_size=100)
            
        # edges
#         nx.draw_networkx_edges(self.__nxGraph,position,edgelist=elarge,width=2)
#         nx.draw_networkx_edges(self.__nxGraph,position,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
        nx.draw_networkx_edges(self.__nxGraph,position,width=2)
        
        # labels
        nx.draw_networkx_labels(self.__nxGraph,position,font_size=20,font_family='sans-serif')
        
        plt.axis('off')
        #plt.savefig("weighted_graph.png") # save as png
#         plt.show(block=False)
        plt.show() # display
        