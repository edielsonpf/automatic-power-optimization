# automatic-power-optimization
Automatic power optmization for wireless sensor networks

For more information, see

"Controle da Topologia de Redes de Sensores sem Fio para Economia de Energia Baseado no Algoritmo de Prim", Revista da Tecnologia da Informação e Comunicação, v. 6, n. 1, pp. 9-14, 2016.

If you use the code, please cite the following [paper](http://rtic.com.br/index.php/rtic/article/view/70):

```
@article{rtic,
	author = {Jonathan de C. Silva e Evandro L. B. Gomes e Edielson P. Frigieri},
	title = {Controle da Topologia de Redes de Sensores sem Fio para Economia de Energia Baseado no Algoritmo de Prim},
	journal = {Revista de Tecnologia da Informação e Comunicação},
	volume = {6},
	number = {1},
	year = {2016},
	keywords = {},
	pages = {9--14},	
	url = {http://rtic.com.br/index.php/rtic/article/view/70}
}
```
# Overview

This is an implementation of an optimization approach based on Prim's algorithm to calculate the minium transmission power for each node part of an Wireless Sensor Network, keeping a valid path between all nodes and the sink node. 

# Quick start

To compute the optimal transmition power vector which results in the minimum spanning tree graph connecting all nodes to the sink with minimum power, use the following steps, which can also be found in the main.py file:

## Step 1: Required libraries

```python

import random, math
from algorithms.mst import MST
from network.wsn import WSN
import logging
```

## Step 2: Constants definition

```python
# Constant definition

logLevel = logging.DEBUG
numNodes = 5
unconnected = 100000
maxPower =  27
minPower = -15
threshold =-80
frequency = 933
area = 50  #square kilometers
```

## Step 3: Create random WSN scenario

```python

# generate random positions (x,y) for each node

nodes=[[random.uniform(0, math.sqrt(area)), random.uniform(0, math.sqrt(area))] for i in range(numNodes)]

```

## Step 4: Initial transmition power definition 

```python
# Defining a transmission power vector with maximum power level for all nodes

powerVector = [maxPower for x in range(numNodes)]
total = sum(powerVector)
print('Initial total power: ' + str(total)+'\n')
````

## Step 5: Calculate the minimum power: method 1

```python
# Creating network object  

Network = WSN(powerVector,numNodes,nodes,frequency,threshold,minPower,logLevel)
Network.plotGraph(positions=None)

print('Optimizing power direct...\n')
powerVector = Network.optimizePower()
Total_I = sum(powerVector)

print('Total power [Phase I]: ' + str(Total_I))
print('Reduction [Phase I]: ' + str((1-(Total_I/total))*100)+'%\n')

```
## Step 6: Calculate the minimum power: method 2 

```python
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



