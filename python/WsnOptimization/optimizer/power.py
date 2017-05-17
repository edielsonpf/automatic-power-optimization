'''
Created on Nov 23, 2015

@author: Edielson
'''
import math
from gurobipy import *

class PowerOptimizer(object):
    '''
    classdocs
    '''
    # Private model object
    model = []
    
    # Decision variables
    PowerTx={}
    y={}
    
    def __init__(self):
        '''
        Constructor
        '''
               
              
    def LoadModel(self,min_power_tx,sensibility,power_vector,graph,links,nodes,loss_function):
                
        self.links = tuplelist(links)
        self.nodes = nodes
        self.min_power_tx = min_power_tx
        self.graph = graph
        self.sensibility = sensibility
        self.loss_function = loss_function
                
        # Create optimization model
        self.model = Model('Power')
        
        for i in self.nodes:
            self.PowerTx[i] = self.model.addVar(vtype=GRB.CONTINUOUS,lb=self.min_power_tx,name='PowerTx[%s]' % (i))
        self.model.update()
        
        for i in self.nodes:
                self.y[i] = self.model.addVar(name='furthest_node[%s]' % (i))
        self.model.update()
         
        self.model.modelSense = GRB.MINIMIZE
        self.model.setObjective(quicksum(self.PowerTx[i] for i in self.nodes))
        self.model.update()
        
           
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
         
        # Further neighbor constraint
        for i in self.nodes:
            for s,d in self.links:
                if i==s:
                    self.model.addConstr(self.y[i] >= self.loss_function(self.graph[s,d]),'[CONST]y[%s,%s]' % (i, d))
        self.model.update()
        
        # Sensibility constraint
        for i in self.nodes:
            self.model.addConstr(self.PowerTx[i] - self.y[i] >= self.sensibility,'[CONST]Sensibility[%s]' % (i))
        self.model.update()
            
                
    def optimize(self):
        
        self.model.write('power.lp')
 
        # Compute optimal solution
        self.model.optimize()
        power_vector=[]
        # Print solution
        if self.model.status == GRB.Status.OPTIMAL:
            solution = self.model.getAttr('x', self.PowerTx)
            for i in self.nodes:
                print('Ptx[%s]: %g' % (i, solution[i]))
                power_vector.append(solution[i])    
        else:
            print('Optimal value not found!\n')
            
        return power_vector;    