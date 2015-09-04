function optimalPowerNet = optimizeNoSteps(powerNet,min_relationNet,min_sensibility,min_power_level)
    
    MIN_LEVEL = -1000000;
    //OPTIMAL_RATE = 10;
    OPTIMAL_RATE = 1;
    [row,col]=size(min_relationNet);
    optimalPowerNet=zeros(size(powerNet));
    //optimize each row
    for i=1:row
        minimum = min_relationNet(i);  
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
