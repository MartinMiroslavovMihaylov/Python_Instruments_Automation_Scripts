function ok=closelu;

global LUHandle;
if ~exist('LUHandle'),
   load LUHandle;
end;
ok=ft2close(double(LUHandle));