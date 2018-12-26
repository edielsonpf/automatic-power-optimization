# Automatic Power Optimization

Automatic power optmization for wireless sensor networks

# Overview

This is an implementation of an optimization approach based on Prim's algorithm to calculate the minium transmission power for each node part of an Wireless Sensor Network, keeping a valid path between all nodes and the sink node. 

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

## Step 3: Create random position for the nodes

```python

# generate random positions (x,y) for each node

nodes=[[random.uniform(0, math.sqrt(area)), random.uniform(0, math.sqrt(area))] for i in range(numNodes)]

```

## Step 4: Define the initial transmition power to maximun for each node 

```python
# Defining a transmission power vector with maximum power level for all nodes

powerVector = [maxPower for x in range(numNodes)]
total = sum(powerVector)
print('Initial total power: ' + str(total)+'\n')
````

## Step 5: Create the intial WSN based on the the defined parameters and positions

```python
# Creating network object  

Network = WSN(powerVector,numNodes,nodes,frequency,threshold,minPower,logLevel)
Network.plotGraph(positions=None)

```
## Step 6: Optimze the WSN 

This final step compares three optimization methods: 

(1) In the method 1, the power of each node is reduced to the possible minimum, just considering its fartest neighbor.

```python

print('Method I: optimizing power direct...\n')
powerVector = Network.optimizePower()
Total_I = sum(powerVector)

print('Total power [Method I]: ' + str(Total_I))
print('Reduction [Method I]: ' + str((1-(Total_I/total))*100)+'%\n')

```


(2) In the method 2, a minimun spanning tree is found an the power of each node is reduced to the possbile minimun, just consireing its fartest neighbor.

```python

print('Method II: finding the minimum spanning tree...\n')
powerVector = Network.optimizeTopology()

print('Optimizing the new graph after MST...\n')
Total_II = sum(powerVector)

print('Total power [Method II]: '+ str(Total_II))
print('Reduction [Method II]: ' + str((1-(Total_II/total))*100)+'%\n')
Network.plotGraph(positions=None)

```
(3) In the method 3, a minimun spanning tree is found an a MIP is solved based on the resulted graph.

```python

print('Method III: optimizing the new graph after MST with MIP model...\n')
powerVectorIII = Network.optimizeTopology2()
print(powerVectorIII)
Total_III = sum(powerVectorIII)

print('Total power [Method III]: '+ str(Total_III))
print('Reduction [Method III]: ' + str((1-(Total_III/total))*100)+'%\n')
Network.plotGraph(positions=None)
```



