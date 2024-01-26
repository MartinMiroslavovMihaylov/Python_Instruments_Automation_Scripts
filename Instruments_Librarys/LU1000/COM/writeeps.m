function ok=writeeps(addr, data);

global EPSHandle;

% pause 2 ms to force gap between write commands to FT232R:
mstic=tic;
mspause=0;
while mspause<0.002,
   mspause=toc(mstic);
end;

%tic;
if EPSHandle>0,
   ok=ft2write(EPSHandle, addr, data);
else
   disp('   ---- Error: no EPSHandle!  ----');
   ok=0;
end;

if ok==0
   disp('   ---- writeeps FAILED!  ----');
end
%toc