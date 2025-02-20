function [ok,diagnosis,handleout,LastDevDescr_in,LastDevDescr_out]=initpm(sel,LastDevDescr)
% initpm(0)                          : show all devices, let user select one
% initpm(1) or initpm() or initpm    : if possible, init last device from LastDevPM.mat
% initpm(2,LastDevDescr)             : init FT2 device LastDevDescr 
% initpm(3,LastDevDescr)             : init FT3 device LastDevDescr 
% Example: initpm(2,'PM1000-100M-XL-FA-NN-D 44')
% In the Python Package, only initpm(2,LastDevDescr) and initpm(3,LastDevDescr) work.
% In Matlab and Octave, all the above works. 

if (nargin<1) || isempty(sel)
   sel=1; % connect to last device
end

diagnosis=0;

if sel
    diagnosis=sel;
end

LastDevFile = 'LastDevPM.mat'; 
existLastDevFile=exist(LastDevFile, 'file');
if existLastDevFile
    diagnosis=diagnosis+4;
end
LastDevType = 0;
if sel<2
    if existLastDevFile && sel
       load(LastDevFile, 'LastDevDescr', 'LastDevType');
    else
       LastDevDescr = ' ';
    end
else
    LastDevType = sel;
end

if ~exist('LastDevDescr', 'var')
   LastDevDescr=' ';
else
   diagnosis=diagnosis+8;
end

LastDevDescr_in=LastDevDescr;

while LastDevType<2 || LastDevType>3
   LastDevType=input('Select USB2.0 (2) or USB3.0 (3) driver: ');
end
if LastDevType==3
    diagnosis=diagnosis+16;
end

switch LastDevType
   case 2
      [ok, handle, LastDevDescr]=ft2init(LastDevDescr);
   case 3
      [ok, handle, LastDevDescr]=ft3init(LastDevDescr);
   otherwise
end

handleout=handle;

LastDevDescr_out=LastDevDescr;

clear global PMHandle
global PMHandle
PMHandle.value = double(handle);
PMHandle.type  = LastDevType;

if ok==1 && sel<2
   save('PMHandle.mat', 'PMHandle', '-v6'); 
   save(LastDevFile, 'LastDevDescr', 'LastDevType', '-v6');
end