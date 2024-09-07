function ok=closeepc;

global EPCHandle;
if ~exist('EPCHandle'),
   load EPCHandle;
end;
ok=ft2close(double(EPCHandle));