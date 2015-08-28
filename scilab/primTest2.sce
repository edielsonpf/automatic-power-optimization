
MIN_ERROR = 0.0001;
MIN_LEVEL = -1000000; 
//define the system constants
NUM_NODES = 5;

// max and min disntaces in km
MAX_DISTANCE = 4;
MIN_DISTANCE = 0.5;

// max power transmission dBm
MAX_POWER = 27;
MIN_POWER = -15;

// min sensibility reception -80dbm
MIN_SENSIBILITY = -80;

//Frequency operation in Mhz
OPERATION_FREQUENCY=933;

//Initializes the nodes location.
nodeLocation = grand(2,NUM_NODES,"unf",MIN_DISTANCE,MAX_DISTANCE);
disp("Nodes location:")
disp(nodeLocation);

//Initializes the power of each node.
nodePower = ones(1,NUM_NODES)*MAX_POWER;
//disp(nodePower);

//Initializes the transmission frequency of each node.
nodeFrequency = ones(1,NUM_NODES)*OPERATION_FREQUENCY;
        
//Calculates the level of each node.
nodeLevel = channelLoss(nodeLocation,nodePower,nodeFrequency,MIN_SENSIBILITY);
disp("Initial nodes level relationship:");
disp(nodeLevel);

plotGraph(nodeLocation,nodeLevel);

newNodeLevel = -1.*nodeLevel;
MAX_LEVEL = -1*MIN_LEVEL;
[newGraph,mincost] = primOptimization(NUM_NODES,newNodeLevel,MAX_LEVEL);
plotGraph2(nodeLocation,newGraph,MAX_LEVEL,'g');
newGraph=-1.*newGraph;
disp('Minimun cost');
disp(mincost);
disp('Minimun graph');
disp(newGraph);
