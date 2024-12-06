function ok=writelu(addr, data);

global LUHandle;

% pause 50 ms to be sure internal RS232-conversion to ITLA-interface is completed
mstic=tic;
mspause=0;
while mspause<0.05,
   mspause=toc(mstic);
end;

%tic;
if LUHandle>0,
   ok=ft2write(LUHandle, addr, data);
else
   disp('   ---- Error: no LUHandle!  ----');
   ok=0;
end;

if ok==0
   disp('   ---- writelu FAILED!  ----');
end
%toc