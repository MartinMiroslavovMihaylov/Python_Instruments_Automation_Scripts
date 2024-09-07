function ok=closepm

global PMHandle
if ~exist('PMHandle')
   load PMHandle;
end
switch PMHandle.type
   case 2
      ok=ft2close(double(PMHandle.value));
   case 3
      ok=ft3close(double(PMHandle.value));
   otherwise
end