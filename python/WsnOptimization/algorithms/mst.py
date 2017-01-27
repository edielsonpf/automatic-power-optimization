'''
Created on Nov 20, 2015

@author: Edielson
'''
import string, logging

class MST(object):
    '''
    classdocs
    '''
    __parent = []
    __key = []
    __mstSet = []
    __infinity = 100000
    __mstGraph = []
    
    def __init__(self, logLevel):
        '''
        Constructor
        '''
        self.__configLog(logLevel)
            
    
    def __configLog(self,logLevel):
        # print a log message to the console.
        logging.basicConfig(format='%(asctime)s %(message)s', level=logLevel)
        
    def printMST(self):
        print('Edge     Cost\n')
        for v in range(len(self.__mstGraph)):
            if v > 0:
                print(str(self.__parent[v]) + ' - ' + str(v) + '    ' + str(self.__mstGraph[v][self.__parent[v]]))
        print('\n')
        
    def __minKey(self,graph):
       
        minKey = self.__infinity
        minIndex = -1
        
        for v in range(len(graph)):
            if (self.__mstSet[v] == False) & (self.__key[v] < minKey):
                minKey = self.__key[v] 
                minIndex = v
        
        return minIndex
        
        
    def prim(self,graph):
         
        self.__parent = [0 for i in range(len(graph))]
        self.__key = [self.__infinity for i in range(len(graph))]
        self.__mstSet = [False for i in range(len(graph))]
        self.__mstGraph = [[self.__infinity for i in range(len(graph))] for j in range(len(graph))]
        
        #Always include first 1st vertex in MST.
        self.__key[0] = 0     # Make key 0 so that this vertex is picked as first vertex
        self.__parent[0] = -1 # First node is always root of MST 
        
        # The MST will have V vertices
        for count in range(len(graph)):
            #Pick the minimum key vertex from the set of vertices not yet included in MST
            u = self.__minKey(graph)
            # Add the picked vertex to the MST Set
            self.__mstSet[u] = True
            
            # Add the new vertex to the MST graph
            if self.__parent[u] >= 0:
                self.__mstGraph[self.__parent[u]][u] = graph[u][self.__parent[u]]          
                        
            # Update key value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are not yet
            # included in MST
            for v in range(len(graph)):
                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if (graph[u][v] != self.__infinity) & (self.__mstSet[v] == False) & (graph[u][v] <  self.__key[v]):
                    self.__parent[v] = u
                    self.__key[v] = graph[u][v]
            
            # must keep connection in both directions
            for i in range(len(self.__mstGraph)):
                for j in range(len(self.__mstGraph)):
                    if self.__mstGraph[i][j] < self.__infinity:
                        self.__mstGraph[j][i] = graph[j][i]
            
        return self.__mstGraph