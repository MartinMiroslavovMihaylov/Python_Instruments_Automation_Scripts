function [res,ok]=readlu(addr)
% readlu now also returns ok, to indicate errors like in init, close, write.
% readlu now also returns results from several addresses, like readeps.

global LUHandle;

% pause 20 ms to force gap between commands:
%mstic=tic;
%mspause=0;
%while mspause<0.02,
%   mspause=toc(mstic);
%end;

if LUHandle>0
   if length(addr)==1
      [ok, res]=ft2read(LUHandle, addr);
   else
      for ii=1:length(addr)
         [ok, res(ii)]=ft2read(LUHandle, addr(ii));
      end
   end 
else
   disp('   ---- Error: no LUHandle!  ----');
   ok=0;
end

if ok==0
   disp('   ---- readlu FAILED!  ----');
   res = 0;
end
  
