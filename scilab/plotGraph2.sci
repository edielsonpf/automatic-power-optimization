function plotGraph2(netLocation, netCost, maxLevel,option)
    
    [a,b]=size(netCost);
    
    plot(nodeLocation(1,:), nodeLocation(2,:),'ro');
     
    for i=1:b
        for j=1:b
           if(i~=j) then
               if netCost(i,j) < maxLevel then
                   x=[nodeLocation(1,i) nodeLocation(1,j)];
                   y=[nodeLocation(2,i) nodeLocation(2,j)];
                   plot(x,y,option)
               end
           end
        end
    end
endfunction
