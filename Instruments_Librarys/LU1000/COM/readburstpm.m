function [dout1, OK] =readburstpm(rdaddr, addrstart, addrstop, wraddr)
% readburstpm now also returns ok, to indicate errors like in init, close, write.

global PMHandle;

switch PMHandle.type
   case 2
      %transferstart=tic;
      [OK, dout1]=ft2readburst(double(PMHandle.value), rdaddr, addrstart, addrstop, wraddr);
      %toc(transferstart)
   case 3
      %transferstart=tic;
      [OK, dout1]=ft3readburst(double(PMHandle.value), rdaddr, addrstart, addrstop, wraddr);
      %toc(transferstart)
   otherwise
end

if OK==0
   disp('   ---- readburstpm FAILED!  ----');
   res = 0;
end
  
%end;
