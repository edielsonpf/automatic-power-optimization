'''
Created on Nov 21, 2015

@author: Edielson
'''

from gurobipy import *

class Flow(object):
    '''
    classdocs
    '''
    __model = 0
    __commodities = 0
    __arcs = 0
    __flow = 0
    
    def __init__(self,commodities,nodes,arcs,capacity,cost,inflow):
        '''
        Constructor
        '''
        self.__loadModel(commodities,nodes,arcs,capacity,cost,inflow)
                
    def __loadModel(self,commodities,nodes,arcs,capacity,cost,inflow):
        
        self.__commodities = commodities
        self.__arcs = arcs
        
        # Create optimization model
        self.__model = Model('Flow')
    
        # Create variables
        self.__flow = {}
        for h in commodities:
            for i,j in arcs:
                self.__flow[h,i,j] = self.__model.addVar(ub=capacity[i,j], obj=cost[h,i,j],name='flow_%s_%s_%s' % (h, i, j))
        self.__model.update()
 
        # Arc capacity constraints
        for i,j in arcs:
            self.__model.addConstr(quicksum(self.__flow[h,i,j] for h in commodities) <= capacity[i,j],'cap_%s_%s' % (i, j))
 
        # Flow conservation constraints
        for h in commodities:
            for j in nodes:
                self.__model.addConstr(quicksum(self.__flow[h,i,j] for i,j in arcs.select('*',j)) + inflow[h,j] ==
                  quicksum(self.__flow[h,j,k] for j,k in arcs.select(j,'*')),'node_%s_%s' % (h, j))
 
        
    def optimize(self):
        
        self.__model.write('flow.lp')
        
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