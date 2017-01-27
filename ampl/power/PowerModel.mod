#########################################################
#			SETS  AND PARAMETERS DEFINITION				#
#########################################################
param n >= 0;

set NODES = 1..n;	# set of nodes

set LINKS within (NODES cross NODES);		# set of links between nodes

param distance {LINKS} >= 0;         		# capacity of each link at primary network  

param connection {LINKS} >= 0;         		# capacity of each link at primary network  

param minLevel;

param dmax >=0;

param nlinks >= 0;


#########################################################
# 				VARIABLES DEFINITION					#
#########################################################

var P{NODES};	#Transmission power per node 

var DIST{NODES} >= 0; #used to identify the most distant node from i

#########################################################
#					MODEL DEFINITION					#
# The objective is to minimize the backup capcity		#
#########################################################

minimize TotalPower: sum{i in NODES} P[i];

#subject to

subject to WorstLink {i in NODES, (i,j) in LINKS}: DIST[i] >= distance[i,j];

subject to MinimumPower {i in NODES}: P[i] >= minLevel + 32.5 + 20*log10(933) + 20*log10(DIST[i]);

