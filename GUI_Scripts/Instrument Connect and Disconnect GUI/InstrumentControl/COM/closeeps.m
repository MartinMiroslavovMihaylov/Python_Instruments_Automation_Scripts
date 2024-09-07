function ok=closeeps;

global EPSHandle;
if ~exist('EPSHandle'),
   load EPSHandle;
end;
ok=ft2close(double(EPSHandle));