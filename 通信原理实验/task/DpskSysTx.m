%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  FileName:            DpskSysTx.m
%  Description:         DPSK通信系统发射机
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Parameter List:       
%       Output Parameter
%           SendBit     比特数据源
%           SendBpsk    差分编码后的BPSK码元
%           SendSig     DPSK已调信号
%           MsgLen      数据源长度
%       Input Parameter
%           Fs          采样率
%           Rs          码元速率
%           SFile       数据源文件
%           SigLen      发送信号长度
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [SendBit,SendBpsk,SendSig,MsgLen]  = DpskSysTx(Fs, Rs, SFile, SigLen)
UpSampleRate=Fs/Rs;
CoderConstraint = 7;%  约束长度 
Rolloff=1;
Preamble=[1 1 1 1 0 1 0 1 1 0 0 1 0 0 0 0];
FilterSymbolLen = 6;

% generate random message
load(SFile); %生成信源比特
MsgLen = length(SendBit);

% convolutoinal coding
trel = poly2trellis(CoderConstraint, [171, 133]);
SendBitWithTail = [SendBit, zeros(size(1 : CoderConstraint - 1))];%  结尾处理, 在消息的结尾添加 coder_constraint-1 个零
code = convenc(SendBitWithTail, trel);%  调用库函数所生成卷积码

% add preamble 
data=[Preamble,code];

% dpsk coding
SendBpsk=zeros(1,length(data)+1);
for iBit=1:length(data)
    SendBpsk(iBit+1)=xor(SendBpsk(iBit),data(iBit));
end

% mapping 0 to +1; 1 to -1
SendBpsk=1-2*SendBpsk;

% upsampling 
SendBpskUp=zeros(1,length(SendBpsk)*UpSampleRate);
for iBits=1:length(SendBpsk)
    SendBpskUp(UpSampleRate*iBits)=SendBpsk(iBits);
end

% RRC filtering
filterDef=fdesign.pulseshaping(UpSampleRate,'Square Root Raised Cosine','Nsym,Beta',FilterSymbolLen,Rolloff);
myFilter = design(filterDef);
myFilter.Numerator=myFilter.Numerator*UpSampleRate;
SendSig = conv(myFilter.Numerator,SendBpskUp);

% 确保信号长度是SigLen
if length(SendSig)>SigLen
    SendSig = 0.7*SendSig(1:SigLen);
elseif length(SendSig)<SigLen
    SendSig = 0.7*[SendSig zeros(1,SigLen-length(SendSig))];
end

