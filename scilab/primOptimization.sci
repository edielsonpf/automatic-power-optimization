function [newGraph,mincost,vertices,maxGraph] = primOptimization(n,cost,maxLevel, minLevel)
    
    [row,col]=size(cost);
    newGraph=zeros(row,col);
    //maxGraph=ones(n,1).*minLevel;
    maxGraph=ones(n,1).*maxLevel;
	for j=1:n
      for i=1:n
//           if (cost(i,j)==0) then
//               cost(i,j)=maxLevel;
//           end
           if (newGraph(i,j)==0) then
               newGraph(i,j)=maxLevel;
           end
        end
    end
    //disp(cost);
    vertices=zeros(2,n-1)';
	visited = zeros(1,n);
    mincost=0;
    ne=1;
    visited(1)=1;
 
    while(ne < n)
		//minimum=maxLevel;
        minimum=minLevel;
        for i=1:n
            for j=1:n
                if((cost(i,j) > minimum) & (cost(i,j) < maxLevel))
                    if(visited(i)~=0)
//                        if(cost(i,j) < maxLevel)
                            minimum=cost(i,j);
                            u=i;
                            a=u
                            v=j;
                            b=v;
  //                      end
                    end
                end
            end
        end
        if((visited(u)==0) | (visited(v)==0))
            disp('Edge:');
            disp(ne);
            disp(u);
            disp(v);
            vertices(ne,1)=a;
            vertices(ne,2)=b;
            disp('cost:');
            disp(minimum);
            ne=ne+1;    
            mincost=mincost+minimum;
            visited(b)=1;
            newGraph(a,b)=minimum;
            newGraph(b,a)=cost(b,a);
            if minimum > maxGraph(a)
                maxGraph(a)=minimum;
            end
            if cost(b,a) > maxGraph(b)
                maxGraph(b)=cost(b,a);
            end    
        end
        cost(b,a)=maxLevel;
        cost(a,b)=cost(b,a);
    end
endfunction
