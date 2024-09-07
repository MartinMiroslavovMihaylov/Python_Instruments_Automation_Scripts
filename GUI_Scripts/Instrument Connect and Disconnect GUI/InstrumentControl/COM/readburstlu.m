function [dout1, OK] =readburstlu(rdaddr, addrstart, addrstop, wraddr)

global LUHandle;

%transferstart=tic;
[OK, dout1]=ft2readburst(LUHandle, rdaddr, addrstart, addrstop, wraddr);
%toc(transferstart)
 
if OK==0
   disp('   ---- readburstlu  FAILED!  ----');
   res = 0;
end
  
%end;
