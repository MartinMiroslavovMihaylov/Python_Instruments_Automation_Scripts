function [ok,diagnosis,handleout,LastDevDescr_in,LastDevDescr_out]=initeps(sel,LastDevDescr)
% initeps(0)                         : show all devices, let user select one
% initeps(1) or initeps() or initeps : if possible, init last device from LastDevEPS.mat
% initeps(2,LastDevDescr)            : init device LastDevDescr 
% Example: initeps(2,'EPS1000-20M-XL-S-FP-LN-D 999')
% In the Python Package, only initeps(2,LastDevDescr) works.
% In Matlab and Octave, all the above works. 

if (nargin<1) || isempty(sel)
   sel=1; % connect to last device
end

diagnosis=0;

if sel
    diagnosis=sel;
end

LastDevFile = 'LastDevEPS.mat'; 
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

global EPSHandle;
EPSHandle=double(handle);

if ok==1 && sel<2
   save('EPSHandle.mat', 'EPSHandle', '-v6'); 
   save(LastDevFile, 'LastDevDescr', '-v6');
end