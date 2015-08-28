MIN_LEVEL = -1000000; 
MAX_LEVEL = -1*MIN_LEVEL;

//Number of nodes
NUM_NODES=6;
//Adjacent cost matrix
cost=[
999 3 1 6 999 999
3 999 5 999 3 999
1 5 999 5 6 4
6 999 5 999 999 2
999 3 6 999 999 6
999 999 4 2 6 999
];
disp("Nodes cost:")
disp(cost);


// max and min disntaces in km
MAX_DISTANCE = 2;
MIN_DISTANCE = 0.5;
//Initializes the nodes location.
nodeLocation = grand(2,NUM_NODES,"unf",MIN_DISTANCE,MAX_DISTANCE);
disp("Nodes location:")
disp(nodeLocation);

plotGraph2(nodeLocation,cost,maxLevel,'b');

[newGraph,mincost] = primOptimization(NUM_NODES,cost,MAX_LEVEL,MIN_LEVEL);

disp('Minimun cost');
disp(mincost);
disp('Minimun graph');
disp(newGraph);
plotGraph2(nodeLocation,newGraph,maxLevel,'g');
