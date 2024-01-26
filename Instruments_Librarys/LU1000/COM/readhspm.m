function [dout1 dout2 dout3 dout4 ok]=readhspm(addr,numaddr)
% readhspm now also returns ok, to indicate errors like in init, close, write.
% %%%: The original while-loop cannot be compiled into Python. 
% So it has been replaced by a for-loop. Original lines see "%%%". 
% In case of error, the while-loop did not finish.
% The for-loop will continue in case of error, 
% but data size will be too small and the returned ok will be 0.
% %%%%: During compilation to Python it was not recognized that dout1, dout2, dout3, dout4
% (usually) have more than 1 element. This gave compilation problems when readhspm
% was called by MeasTable and MeasTable was called by another script: 
% The individual elements of the returned dout1, dout2, dout3, dout4 could
% not be addressed. To solve the problem the original lines "%%%%" were replaced. 
% That replacement has the additional advantage that error results are marked as NaN.

global PMHandle;

ok=0;

switch PMHandle.type
   case 2
      buffer_bytes=2^16;
   case 3
      buffer_bytes=2^12;
   otherwise
end

buffer_addr = buffer_bytes/8; % 64 bits per addr

addrtransferred=0;
curaddr = addr;

dout1=NaN(1,numaddr);
dout2=NaN(1,numaddr);
dout3=NaN(1,numaddr);
dout4=NaN(1,numaddr);
%%%%dout1=[];
%%%%dout2=[];
%%%%dout3=[];
%%%%dout4=[];

for addrtransferred=0:buffer_addr:numaddr-1
%%%while addrtransferred<numaddr

    curnumaddr = min(buffer_addr, numaddr-addrtransferred);

    switch PMHandle.type
       case 2
          [ok, curdout1 curdout2 curdout3 curdout4]=ft2readhs(PMHandle.value, curaddr, curnumaddr);
       case 3
          [ok, curdout1 curdout2 curdout3 curdout4]=ft3readhs(PMHandle.value, curaddr, curnumaddr);
       otherwise
    end
   
   %toc(transferstart)
 
   if ok==0
        disp('---- readhspm FAILED! ----');
   else
       addr1=addrtransferred+1;
       addr2=addrtransferred+curnumaddr;
       dout1(addr1:addr2) = curdout1;
       dout2(addr1:addr2) = curdout2;
       dout3(addr1:addr2) = curdout3;
       dout4(addr1:addr2) = curdout4;
       
       %%%%dout1 = [dout1 curdout1];
       %%%%dout2 = [dout2 curdout2];
       %%%%dout3 = [dout3 curdout3];
       %%%%dout4 = [dout4 curdout4];
       curaddr = curaddr + curnumaddr;
       %%%addrtransferred = addrtransferred + curnumaddr;
   end
  
end
