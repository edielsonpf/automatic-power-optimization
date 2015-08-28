function result = validateConnections(initialNet,finalNet)
    
    result = 0;
    MIN_LEVEL = -1000000;
    [row,col]=size(initialNet);
    for i=1:row
        for j=1:col
            if initialNet(i,j)~=MIN_LEVEL then
                if  finalNet(i,j)== MIN_LEVEL then
                    result = 1;
                    break;
                end
            end
        end
        if result == 1 then
            break;
        end  
    end
endfunction
