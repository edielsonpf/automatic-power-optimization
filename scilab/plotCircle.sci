function plotCircle(netLocation, nodesPower, nodesFrequency, min_sensibility)
    
    [a,b]=size(nodesPower);
    
    plot(nodeLocation(1,:), nodeLocation(2,:),'ro');
     
    for i=1:b
       //loss = 32.5 + 20*log10(d) + 20*log10(nodes_frequency(i));
       loss = nodesPower(i)-min_sensibility;
       d=10^((loss-32.5-20*log10(nodesFrequency(i)))/20);
       x=nodeLocation(1,i)+d*cos(0:.1:2*%pi);
       y=nodeLocation(2,i)+d*sin(0:.1:2*%pi);
       plot2d(x,y,i);
    end
endfunction
