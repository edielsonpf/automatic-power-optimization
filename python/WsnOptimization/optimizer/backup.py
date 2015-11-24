'''
Created on Nov 23, 2015

@author: Edielson
'''
import math
from gurobipy import *

class Backup(object):
    '''
    classdocs
    '''
    __model = 0
    __links = 0
    __bCapacity = []
    __bLinks = []
    
    def __init__(self,nodes,links,capacity,cost,mean,variance,e):
        '''
        Constructor
        '''
        self.__loadModel(nodes,links,capacity,cost)
                
    def __loadModel(self,nodes,links,capacity,cost,mean,variance,invstd):
        
        self.__links = links
        
        # Create optimization model
        self.__model = Model('Backup')
    
        # Create variables
        self.__bCapacity = {}
        self.__bLinks = {}
        
        for i,j in links:
            self.__bCapacity[i,j] = self.__model.addVar(ub=capacity[i,j], obj=cost[i,j],name='BackupCapacity_%s_%s' % (i, j))
        
        for i,j in links:
            for s,d in links:
                self.__bLinks[i,j,s,d] = self.__model.addVar(ub=capacity[i,j], obj=cost[i,j],name='backup_link_%s_%s_%s_%s' % (i, j, s, d))
        
        self.__model.update()
 
        # Link capacity constraints
        for i,j in links:
            self.__model.addConstr(self.__bCapacity[i,j] >= quicksum((mean[s,d]+math.sqrt(variance[s,d])*invstd)*self.__bLinks[i,j,s,d]*capacity[s,d] for (s,d) in links),'cap_%s_%s' % (i, j))
 
        # Flow conservation constraints
        for s,d in links:
            self.__model.addConstr(quicksum(self.__bLinks[i,j,s,d] for i,j in links.select(i==s,j)) - 
                quicksum(self.__bLinks[j,i,s,d] for j,i in links.select(j,i==s)),'node_%s_%s' % (s, d) == 1)
 
        # Flow conservation constraints
        for s,d in links:
            self.__model.addConstr(quicksum(self.__bLinks[i,j,s,d] for i,j in links.select(i==d,j)) - 
                quicksum(self.__bLinks[j,i,s,d] for j,i in links.select(j,i==d)),'node_%s_%s' % (s, d) == -1)
            
        # Flow conservation constraints
        for s,d in links:
            self.__model.addConstr(quicksum(self.__bLinks[i,j,s,d] for i,j in links.select(i!=s & i!=d,j)) - 
                quicksum(self.__bLinks[j,i,s,d] for j,i in links.select(j,i!=s & i!=d)),'node_%s_%s' % (s, d) == 0)
        
    def optimize(self):
        
        # Compute optimal solution
        self.__model.optimize()
 
        # Print solution
        if self.__model.status == GRB.Status.OPTIMAL:
            solution = self.__model.getAttr('x', self.__flow)
            for h in self.__commodities:
                print('\nOptimal flows for %s:' % h)
                for i,j in self.__arcs:
                    if solution[h,i,j] > 0:
                        print('%s -> %s: %g' % (i, j, solution[h,i,j]))    