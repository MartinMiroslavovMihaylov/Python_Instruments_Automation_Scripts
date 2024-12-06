function ok=writepm(addr,data)

global PMHandle;

% pause 2 ms to force gap between commands:
%mstic=tic;
%mspause=0;
%while mspause<0.002,
%   mspause=toc(mstic);
%end;

%tic;
switch PMHandle.type
   case 2
      ok=ft2write(double(PMHandle.value), addr, data);
   case 3
      ok=ft3write(double(PMHandle.value), addr, data);
   otherwise
end

if ok==0
   disp('   ---- writepm FAILED!  ----');
end
%toc