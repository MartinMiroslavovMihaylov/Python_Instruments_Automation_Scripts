function ok=writeepc(addr, data);

global EPCHandle;

% pause 2 ms to force gap between write commands to FT232R:
mstic=tic;
mspause=0;
while mspause<0.002,
   mspause=toc(mstic);
end;

%tic;
if EPCHandle>0,
   ok=ft2write(EPCHandle, addr, data);
else
   disp('   ---- Error: no EPCHandle!  ----');
   ok=0;
end;

if ok==0
   disp('   ---- writeepc FAILED!  ----');
end
%toc