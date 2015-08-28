function AvgPower=NetPower(nodesPower)
     [row,col]=size(nodesPower);
     AvgPower=0;
     NumNodes=0;
     for i=1:col
        AvgPower=AvgPower+nodesPower(i);
        NumNodes=NumNodes+1;
     end
     //AvgPower=AvgPower/NumNodes;
endfunction
