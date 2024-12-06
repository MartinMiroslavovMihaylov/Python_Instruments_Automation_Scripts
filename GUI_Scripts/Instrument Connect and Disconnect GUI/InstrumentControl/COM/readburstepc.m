
function [dout1, OK] =readburstepc(rdaddr, addrstart, addrstop, wraddr);

global EPCHandle;

%transferstart=tic;
[OK, dout1]=ft2readburst(EPCHandle, rdaddr, addrstart, addrstop, wraddr);
%toc(transferstart)
 
if OK==0,
   disp('   ---- readburstepc FAILED!  ----');
   res = 0;
end;
  
%end;
