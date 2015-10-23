function [newGraph,maxcost,vertices,maxGraph] = MaxST(n,cost,maxLevel, minLevel)
    
    [row,col]=size(cost);

    newGraph=ones(row,col).*minLevel;
    maxGraph=ones(n,1).*maxLevel;
    
    vertices=zeros(2,n-1)';
	visited = zeros(1,n);
    maxcost=0;
    ne=1;
    visited(1)=1;
 
    while(ne < n)
		maximum=minLevel;
        for i=1:n
            for j=1:n
                if(cost(i,j) > maximum)
                    if(visited(i)~=0)
                        if(cost(j,i) > minLevel)
                            maximum=cost(i,j);
                            u=i;
                            a=u
                            v=j;
                            b=v;
                        end
                    end
                end
            end
        end
        if((visited(u)==0) | (visited(v)==0))
            disp('Edge:');
            disp(ne);
            disp(a);
            disp(b);
            vertices(ne,1)=a;
            vertices(ne,2)=b;
            disp('cost:');
            disp(maximum);
            ne=ne+1;    
            maxcost=maxcost+maximum;
            visited(b)=1;
            newGraph(a,b)=maximum;
            newGraph(b,a)=cost(b,a);
            if maximum < maxGraph(a)
                maxGraph(a)=maximum;
            end
            if cost(b,a) < maxGraph(b)
                maxGraph(b)=cost(b,a);
            end    
        end
        cost(b,a)=minLevel;
        cost(a,b)=cost(b,a);
    end
endfunction
