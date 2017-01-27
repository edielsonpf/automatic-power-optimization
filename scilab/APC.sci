// Simulador de colônia de pássaros na solução de problemas.
// Baseado no artigo Partical Swarm Optimization de James Kennedy.
//
// Por Edielson Prevato Frigieri
   function APC() 
    //Limpa qualquer variável criada em outra simulação.
    clear;
    //fecha todos os gráficos
    xdel(winsid());
    
    //define the system constants
    MIN_ERROR = 0.001;
    MIN_LEVEL = -1000000; 
    MAX_LEVEL = 27; 
    
    // max power transmission dBm
    MAX_POWER = 27;
    MIN_POWER = -15;
        
    //10, 15, 20
    // max and min distances in km
    MAX_DISTANCE = 20;
    MIN_DISTANCE = 1;
    AREA=MAX_DISTANCE^2;
    
    //10% ~ 80%
    //AVERAGE_DISTANCE=20;
    //STD_DISTANCE=AVERAGE_DISTANCE*0.3;
    
    //10%, 30%, 60%, 80%
    NODES_DENSITY=0.1;   
    //40,120,240,320
    NUM_NODES = round(AREA*NODES_DENSITY);
        
    // min sensibility reception -80dbm
    MIN_SENSIBILITY = -80;
        
    //Frequency operation in Mhz
    OPERATION_FREQUENCY=933;
    
    //Initializes the nodes location.
        //Uniform distribution
    nodeLocation = grand(2,NUM_NODES,"unf",MIN_DISTANCE,MAX_DISTANCE);
        //Normal distribution
    //nodeLocation = grand(2,NUM_NODES,"nor",AVERAGE_DISTANCE,STD_DISTANCE);
    //disp("Nodes location:")
    //disp(nodeLocation);
    //nodeLocation=csvRead('NodeLocationInit.csv');
    
    //Initializes the power of each node.
    nodePower = ones(1,NUM_NODES)*MAX_POWER;
    //disp(nodePower); //uncomment for debuging
    
    //Initializes the transmission frequency of each node.
    nodeFrequency = ones(1,NUM_NODES)*OPERATION_FREQUENCY;
    write_csv(nodeFrequency, 'NodeFrequency.csv');        
    
    //Calculates the level of each node.
    nodeLevel = channelLoss(nodeLocation,nodePower,nodeFrequency,MIN_SENSIBILITY);
    //disp("Initial nodes level relationship:");
    //disp(nodeLevel);
    write_csv(nodeLevel, 'InitialNodeLevel.csv');
    
   //ploting resulted graph
   figure;
   plotGraph(nodeLocation,nodeLevel,'b'); //uncomment for debuging
   xlabel("Km");
   ylabel("Km");  
   //Calculating the network average power
   //disp('The initial power sum:');
   AvgPower=NetPower(nodePower);
   disp(AvgPower);
   
   eqm = 100;
   LastAvgPower = AvgPower; 
   LastNodeLevel = nodeLevel;
   LastNodePower = nodePower;
   numSteps=1;
   Power(numSteps)=AvgPower;
   
   tic();
   
   //while eqm > MIN_ERROR
       
       //disp('Step:');
       //disp(numSteps);
       
       //Calculates the level of each node.
       nodeLevel = channelLoss(nodeLocation,nodePower,nodeFrequency,MIN_SENSIBILITY);
       //disp('Node Level before prim:');
       //disp(nodeLevel);
       //=========================================
       //Calculating the path with lowest cost in the graph using prim algorithm
       //nodeLevel = -1.*nodeLevel;
       //max_level = -1*MIN_LEVEL;
       max_level = MAX_LEVEL;
       //min_level = -1*MAX_LEVEL;
       min_level = MIN_LEVEL;
       //[newGraph,mincost,vertices,maxGraph] = primOptimization(NUM_NODES,nodeLevel,max_level,min_level);
       [newGraph,mincost,vertices,maxGraph] = MaxST(NUM_NODES,nodeLevel,max_level,min_level);
       //nodeLevel=-1.*newGraph;
       nodeLevel=newGraph;
       //min_nodeLevel = -1.*maxGraph;
       min_nodeLevel = maxGraph;
       //disp(vertices);
       //disp("Nodes level relationship after prim algorithm:")
       //disp(nodeLevel);
       //disp(-1.*maxGraph);
       //=========================================
       
       nodePower = optimizeNoSteps(nodePower,nodeLevel,min_nodeLevel,MIN_SENSIBILITY,MIN_POWER);
       //nodePower = optimize(nodePower,min_nodeLevel,MIN_SENSIBILITY,MIN_POWER);
               
       //Calculating the network average power
       NewAvgPower=NetPower(nodePower);
              
       eqm = (LastAvgPower-NewAvgPower)^2;
       LastAvgPower = NewAvgPower;
       numSteps=numSteps+1;
       Power(numSteps)=LastAvgPower;
   //end
   
   time=toc();
   
   //ploting resulted graph
   //plotGraph2(nodeLocation,-1.*nodeLevel,MAX_LEVEL,'g');
      
   nodeLevel = channelLoss(nodeLocation,nodePower,nodeFrequency,MIN_SENSIBILITY);
   disp('###End of optimization###');
   //disp('Total number of steps:');
   //disp(numSteps);
   //disp("Final nodes level relationship:")
   //disp(nodeLevel);
   
   disp('The final power sum:'); 
   NewAvgPower=NetPower(nodePower);
   disp(NewAvgPower);
       
   disp('Power reduction (dBm):');
   Reduction = AvgPower-LastAvgPower;
   disp(Reduction);
   disp('Power reduction(%):');
   PercReduction = 1-((LastAvgPower+Reduction)/(AvgPower+Reduction));
   disp(PercReduction*100);
   
   disp('Time (seconds):');
   disp(time);
   
   write_csv(nodeLocation, 'NodeLocation.csv');
   write_csv(nodeLevel,'NodeLevel.csv');
   
   //ploting resulted graph
   //plotGraph(nodeLocation,nodeLevel,'g');
   
   figure;
   plotGraph(nodeLocation,nodeLevel,'b');
   
   figure;
   //plotGraph(nodeLocation,nodeLevel,'b');
   plotCircle(nodeLocation,nodePower,nodeFrequency,MIN_SENSIBILITY);
   
   //disp('Optimal power per radio:');
   //disp(nodePower);
   write_csv(nodePower, 'NodePower.csv');        
   //=========================================
   //figure;
   //plot(Power);
endfunction
