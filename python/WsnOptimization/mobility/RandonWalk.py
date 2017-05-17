from pymobility.models.mobility import random_waypoint

import matplotlib.pyplot as plt
#import time

# number of nodes
nr_nodes = 10

# simulation area (units)
MAX_X, MAX_Y = 100, 100

# max and min velocity
MIN_V, MAX_V = 0.1, 1.

# max waiting time
MAX_WT = 1.0

#plt.ion()
#ax = plt.subplot(111)
#line, = ax.plot(range(MAX_X), range(MAX_Y), linestyle='', marker='.')

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion() 

"""This will create a Random Waypoint instance with 200 nodes in a simulation 
area of 100x100 units, velocity chosen from a uniform distribution between 0.1
and 1.0 units/step and maximum waiting time of 1.0 steps. This object is a 
generator that yields the position of the nodes in each step. 
"""
rw = random_waypoint(nr_nodes, dimensions=(MAX_X, MAX_Y), velocity=(MIN_V, MAX_V), wt_max=MAX_WT)


#positions = next(rw)
#print positions

step=0
for positions in rw:
    print('Step %d' %step)
    print positions
    step+=1
#    line.set_data(positions[:,0],positions[:,1])
#    plt.draw()
    plt.cla()
    ax.scatter(positions[:,0], positions[:,1], c='r', marker='o')
    plt.axis([0.0, MAX_X, 0, MAX_Y]) 
    plt.pause(0.0001)