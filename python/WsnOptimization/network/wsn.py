'''
Created on Nov 20, 2015

@author: Edielson
'''
import random, math, logging

class WSN(object):
    '''
    classdocs
    '''
    __area = 0
    __numNodes = 0
    __threshold = 0
    __unconnected = 100000
    __nodes = []
    __power = []
    __graph = []
    
    def __init__(self,power,numNodes,frequency,threshold,area,minTxLevel,log):
        '''
        Constructor
        '''
        self.__area = area
        self.__frequency = frequency
        self.__numNodes = numNodes
        self.__threshold = threshold
        self.__power = power
        self.__minTxLevel = minTxLevel
        self.__configLog(log)
            
    
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
        
    def generateScenario(self):
        
        # generate random positions (x,y) for each node
        self.__nodes=[[random.uniform(0, math.sqrt(self.__area)) for i in range(self.__numNodes)] for i in range(2)]
       
        # generated a graph with connection between nodes initially unconnected
        graph = [[self.__unconnected for i in range(self.__numNodes)] for i in range(self.__numNodes)]
        
        ValidConnection = False
        
        for i in range(self.__numNodes):
            for j in range(self.__numNodes):
                if i != j:
                    dist = math.sqrt(((self.__nodes[0][i]-self.__nodes[0][j])**2)+((self.__nodes[1][i]-self.__nodes[1][j])**2))
                    if dist < self.__caldDistance(self.__power[0][i]):
                        ValidConnection = True
                        graph[i][j] = dist 
        
        if ValidConnection == False:
            logging.warning('The graph is not connected!')
            graph = []

        return graph
    
    def getScenario(self):
        return self.__nodes
    
    def optimize(self,graph):
        #optimize each row, finding the farthest node
        for i in range(len(graph)):
            highDistance = 0
            for j in range(len(graph)):
                if (i!=j) & (graph[i][j] < self.__unconnected) & (graph[i][j] > highDistance):
                    highDistance = graph[i][j]  

            #calculate the power of the transmitter for achieving the minimum power level 
            self.__power[i] = self.__threshold+self.__calcLoss(highDistance);
            if self.__power[i] < self.__minTxLevel:
                self.__power[i] = self.__minTxLevel
        
        return self.__power
    
    def getLinks(self,graph):
        
        links = []
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[i][j] < self.__unconnected:
                    links.append((i,j))
        return links