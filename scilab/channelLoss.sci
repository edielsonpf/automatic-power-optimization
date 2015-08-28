function nodes_level = channelLoss(nodes_location, nodes_power, nodes_frequency, min_sensibility)
     
   MIN_LEVEL = -1000000;
      
   [a,b]=size(nodes_location);
     
    nodes_relation = zeros(b,b);
     
    for i=1:b
        for j=1:b
           if i~=j then
               d=sqrt(((nodes_location(1,i)-nodes_location(1,j))^2)+((nodes_location(2,i)-nodes_location(2,j))^2));
               //disp("d["+string(i)+"]["+string(j)+"]="+string(d));
               loss = 32.5 + 20*log10(d) + 20*log10(nodes_frequency(i));
               nodes_level(i,j)= nodes_power(i) - loss;
               if nodes_level(i,j)< min_sensibility then
                    nodes_level(i,j) = MIN_LEVEL; 
               end
           else
               nodes_level(i,j)=MIN_LEVEL;
           end
        end
    end
endfunction
