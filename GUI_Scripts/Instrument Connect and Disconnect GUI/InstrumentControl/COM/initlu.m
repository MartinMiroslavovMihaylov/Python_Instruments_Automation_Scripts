function [ok,diagnosis,handleout,LastDevDescr_in,LastDevDescr_out]=initlu(sel,LastDevDescr)
% initlu(0)                          : show all devices, let user select one
% initlu(1) or initlu() or initlu    : if possible, init last device from LastDevLU.mat
% initlu(2,LastDevDescr)             : init device LastDevDescr 
% Example: initlu(2,'LU1000-CC-FP-L-D 00020')
% In the Python Package, only initlu(2,LastDevDescr) works.
% In Matlab and Octave, all the above works. 

if (nargin<1) || isempty(sel)
   sel=1; % connect to last device
end

diagnosis=0;

if sel
    diagnosis=sel;
end

LastDevFile = 'LastDevLU.mat'; 
existLastDevFile=exist(LastDevFile, 'file');
if existLastDevFile
    diagnosis=diagnosis+4;
end
if sel<2
    if existLastDevFile && sel
       load(LastDevFile, 'LastDevDescr');
    else
       LastDevDescr=' ';
    end
end

if ~exist('LastDevDescr', 'var')
   LastDevDescr=' ';
else
   diagnosis=diagnosis+8;
end

LastDevDescr_in=LastDevDescr;

[ok, handle, LastDevDescr]=ft2init(LastDevDescr);

handleout=handle;

LastDevDescr_out=LastDevDescr;

global LUHandle;
LUHandle=double(handle);

if ok==1 && sel<2
   save('LUHandle.mat', 'LUHandle', '-v6'); 
   save(LastDevFile, 'LastDevDescr', '-v6');
end