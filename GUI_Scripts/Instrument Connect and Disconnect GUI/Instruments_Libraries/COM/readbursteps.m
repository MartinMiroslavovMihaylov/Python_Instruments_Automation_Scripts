
function [dout1, OK] =readbursteps(rdaddr, addrstart, addrstop, wraddr);

global EPSHandle;

%transferstart=tic;
[OK, dout1]=ft2readburst(EPSHandle, rdaddr, addrstart, addrstop, wraddr);
%toc(transferstart)
 
if OK==0,
   disp('   ---- readbursteps FAILED!  ----');
   res = 0;
end;
  
%end;
