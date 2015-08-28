function plotGraph(nodeLocation, netCost)
    
    MIN_LEVEL = -1000000;
    [a,b]=size(netCost);
    
    figure;
    plot(nodeLocation(1,:), nodeLocation(2,:),'ro');
     
    for i=1:b
        for j=1:b
           if(i~=j) then
               if netCost(i,j) > MIN_LEVEL then
                   x=[nodeLocation(1,i) nodeLocation(1,j)];
                   y=[nodeLocation(2,i) nodeLocation(2,j)];
                   plot(x,y)
               end
           end
        end
    end
endfunction
