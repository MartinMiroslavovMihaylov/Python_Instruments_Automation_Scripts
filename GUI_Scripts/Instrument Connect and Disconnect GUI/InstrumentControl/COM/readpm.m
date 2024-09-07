function [res,ok]=readpm(addr)
% readpm now also returns ok, to indicate errors like in init, close, write.

global PMHandle;

% pause 2 ms to force gap between commands:
%mstic=tic;
%mspause=0;
%while mspause<0.002,
%   mspause=toc(mstic);
%end;

switch PMHandle.type
   case 2
      [ok , res]=ft2read(double(PMHandle.value), addr);
   case 3
      [ok , res]=ft3read(double(PMHandle.value), addr);
   otherwise
end

if ok==0
   disp('---- readpm   FAILED! ----');
   res = 0;
end
  
