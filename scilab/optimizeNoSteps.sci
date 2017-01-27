function optimalPowerNet = optimizeNoSteps(powerNet,relationNet,min_relationNet,min_sensibility,min_power_level)

    USE_HASH = 1;    
    MIN_LEVEL = -1000000;
    //OPTIMAL_RATE = 10;
    OPTIMAL_RATE = 1;
    
    optimalPowerNet=zeros(size(powerNet));
    //optimize each row
    disp(relationNet);
if USE_HASH == 1    
    [row,col]=size(min_relationNet);
else
    [row,col]=size(relationNet);
end
    //optimize each row
    for i=1:row
if USE_HASH == 1    
        minimum = min_relationNet(i);  
        //get the minimum power
else
        minimum = 0;
        for j=1:col
            if (i~=j)&(relationNet(i,j)> min_sensibility) then
            //if (i~=j) then
                if  (relationNet(i,j) < minimum) then
                    minimum = relationNet(i,j);  
                end
            end    
        end
end    
        //if minimum > MIN_LEVEL then
            // calculate the power of the transmitter for achieving the minimum power level 
            loss = powerNet(i) - minimum;
            minPower = min_sensibility+loss;
            //if ((minPower) < powerNet(i)) then
                if minPower > min_power_level then
                    optimalPowerNet(i) = minPower;
                else
                    optimalPowerNet(i) = min_power_level;
                end
            //else
            //    optimalPowerNet(i)=powerNet(i);
            //end
        //end
    end
endfunction
