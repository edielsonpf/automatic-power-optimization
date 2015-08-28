function generate_schema() 
    MAX_DISTANCE = 5;
    MIN_DISTANCE = 1;
    AREA=MAX_DISTANCE^2;
    
    //10% ~ 80%
    //AVERAGE_DISTANCE=20;
    //STD_DISTANCE=AVERAGE_DISTANCE*0.3;
    
    //10%, 30%, 60%, 80%
    NODES_DENSITY=0.1;   
    //40,120,240,320
    NUM_NODES = round(AREA*NODES_DENSITY);
 
    //Initializes the nodes location.
        //Uniform distribution
    nodeLocation = grand(2,NUM_NODES,"unf",MIN_DISTANCE,MAX_DISTANCE);
    write_csv(nodeLocation, 'NodeLocation_StdOrder01.csv');
endfunction