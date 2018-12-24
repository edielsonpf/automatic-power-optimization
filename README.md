# automatic-power-optimization
Automatic power optmization for wireless sensor networks

For more information, see

"Controle da Topologia de Redes de Sensores sem Fio para Economia de Energia Baseado no Algoritmo de Prim", Revista da Tecnologia da Informação e Comunicação, v. 6, n. 1, pp. 9-14, 2016.

https://www.researchgate.net/publication/302596670_Controle_da_Topologia_de_Redes_de_Sensores_sem_Fio_para_Economia_de_Energia_Baseado_no_Algoritmo_de_Prim 

# Quick start

```python

import random, math
from algorithms.mst import MST
from network.wsn import WSN
import logging

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

nodes=[[random.uniform(0, math.sqrt(area)), random.uniform(0, math.sqrt(area))] for i in range(numNodes)]

# Defining a transmission power vector with maximum power level for all nodes

powerVector = [maxPower for x in range(numNodes)]
total = sum(powerVector)
print('Initial total power: ' + str(total)+'\n')

# Creating network object  

Network = WSN(powerVector,numNodes,nodes,frequency,threshold,minPower,logLevel)
Network.plotGraph(positions=None)

print('Optimizing power direct...\n')
powerVector = Network.optimizePower()
Total_I = sum(powerVector)

print('Total power [Phase I]: ' + str(Total_I))
print('Reduction [Phase I]: ' + str((1-(Total_I/total))*100)+'%\n')

#====================================================================

print('Finding the minimum spanning tree...\n')
powerVector = Network.optimizeTopology()

print('Optimizing the new graph after MST...\n')
Total_II = sum(powerVector)

print('Total power [Phase II]: '+ str(Total_II))
print('Reduction [Phase II]: ' + str((1-(Total_II/total))*100)+'%\n')
Network.plotGraph(positions=None)

print('Optimizing the new graph after MST with MIP model...\n')
powerVectorIII = Network.optimizeTopology2()
print(powerVectorIII)
Total_III = sum(powerVectorIII)

print('Total power [Phase III]: '+ str(Total_III))
print('Reduction [Phase III]: ' + str((1-(Total_III/total))*100)+'%\n')
```



