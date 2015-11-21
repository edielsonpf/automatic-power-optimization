'''
Created on Nov 20, 2015

@author: Edielson
'''
import random, math, logging

class scenarioWSN(object):
    '''
    classdocs
    '''
    __minArea = 0
    __maxArea = 0
    __numNodes = 0
    __maxDist = 0
    __uncValue = 0
    __nodes = []
    __connectGraph = []

    def __init__(self, minArea,maxArea,numNodes,maxDist,uncValue,logLevel):
        '''
        Constructor
        '''
        self.__maxArea = maxArea
        self.__minArea = minArea
        self.__numNodes = numNodes
        self.__maxDist = maxDist
        self.__uncValue = uncValue
        self.__configLog(logLevel)
            
    
    def __configLog(self,logLevel):
        # print a log message to the console.
        logging.basicConfig(format='%(asctime)s %(message)s', level=logLevel)
        
    def generate(self):
        
        # generate random positions (x,y) for each node
        self.__nodes=[[random.uniform(self.__minArea, self.__maxArea) for i in range(self.__numNodes)] for i in range(2)]
        # generated a graph with connection between nodes initially unconnected
        self.__connectGraph = [[self.__uncValue for i in range(self.__numNodes)] for i in range(self.__numNodes)]
        
        ValidConnection = False
        
        for i in range(self.__numNodes):
            for j in range(self.__numNodes):
                if i != j:
                    dist = math.sqrt(((self.__nodes[0][i]-self.__nodes[0][j])**2)+((self.__nodes[1][i]-self.__nodes[1][j])**2))
                    if dist < self.__maxDist:
                        ValidConnection = True
                        self.__connectGraph[i][j] = dist 
        
        if ValidConnection == False:
            logging.warning('The graph is not connected!')
            self.__connectGraph = []

        return self.__connectGraph
    
    def getScenario(self):
        return self.__nodes
    