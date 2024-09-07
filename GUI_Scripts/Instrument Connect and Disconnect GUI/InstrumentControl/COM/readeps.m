function [res,ok]=readeps(addr)
% readeps now also returns ok, to indicate errors like in init, close, write.
% readeps now also returns results from several addresses.

global EPSHandle;

% pause 2 ms to force gap between commands:
%mstic=tic;
%mspause=0;
%while mspause<0.002,
%   mspause=toc(mstic);
%end;


if EPSHandle>0
   if length(addr)==1
      [ok, res]=ft2read(EPSHandle, addr);
   else
      for ii=1:length(addr)
         [ok, res(ii)]=ft2read(EPSHandle, addr(ii));
      end
   end 
else
   disp('   ---- Error: no EPSHandle!  ----');
   ok=0;
end

if ok==0
   disp('   ---- readeps FAILED!  ----');
   res = 0;
end
  
