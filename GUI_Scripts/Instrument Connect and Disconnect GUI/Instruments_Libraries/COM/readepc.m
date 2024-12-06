function [res,ok]=readepc(addr)
% readepc now also returns ok, to indicate errors like in init, close, write.
% readepc now also returns results from several addresses, like readeps.

global EPCHandle;

% pause 2 ms to force gap between commands:
%mstic=tic;
%mspause=0;
%while mspause<0.002,
%   mspause=toc(mstic);
%end;


if EPCHandle>0
   if length(addr)==1
      [ok, res]=ft2read(EPCHandle, addr);
   else
      for ii=1:length(addr)
         [ok, res(ii)]=ft2read(EPCHandle, addr(ii));
      end
   end 
else
   disp('   ---- Error: no EPCHandle!  ----');
   ok=0;
end

if ok==0
   disp('   ---- readepc FAILED!  ----');
   res = 0;
end
  
