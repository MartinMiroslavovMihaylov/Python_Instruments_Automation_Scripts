function [dout,ok]=readfrpm(block);
% readfrpm now also returns ok, to indicate errors like in init, close, write.

global PMHandle;

% pause 2 ms to force gap between commands:
mstic=tic;
mspause=0;
while mspause<0.002
   mspause=toc(mstic);
end

switch PMHandle.type
   case 2
      [ok, dout]=ft2readfr(double(PMHandle.value), block);
   case 3
      [ok, dout]=ft3readfr(double(PMHandle.value), block);
   otherwise
end
 
if ok==0
   disp('   ---- readfrpm FAILED!  ----');
   dout=0;
end
