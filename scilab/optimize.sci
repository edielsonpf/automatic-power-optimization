function optimalPowerNet = optimize(powerNet,min_relationNet,min_sensibility,min_power_level)
    
    MIN_LEVEL = -1000000;
    //OPTIMAL_RATE = 10;
    OPTIMAL_RATE = 1;
    [row,col]=size(min_relationNet);
    optimalPowerNet=zeros(size(powerNet));
    //optimize each row
    for i=1:row
        minimum = min_relationNet(i);  
        if minimum > MIN_LEVEL then
            // calculate the power of the transmitter for achieving the minimum power level 
            loss = powerNet(i) - minimum;
            newPowerLevel =  powerNet(i)-rand()*OPTIMAL_RATE;
            if ((newPowerLevel - loss) > min_sensibility) then
                if newPowerLevel > min_power_level then
                    optimalPowerNet(i) = newPowerLevel;
                else
                    optimalPowerNet(i) = min_power_level;
                end
            else
                optimalPowerNet(i)=powerNet(i);
            end
        end
    end
endfunction
