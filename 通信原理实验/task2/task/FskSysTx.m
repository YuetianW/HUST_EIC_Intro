%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  FileName:            FskSysTx.m
%  Description:         FSK通信系统发射机
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Parameter List:       
%       Output Parameter
%           SendBit     比特数据源
%           SendSig     DPSK已调信号
%           MsgLen      数据源长度
%       Input Parameter
%           Fs          采样率
%           Rs          码元速率
%           SFile       数据源文件
%           SigLen      发送信号长度
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [SendBit,SendSig,MsgLen]  = FskSysTx(Fs, Rs, SFile, SigLen)
UpSampleRate=Fs/Rs;
CoderConstraint = 7;%  约束长度 
Preamble=[1 1 1 1 0 1 0 1 1 0 0 1 0 0 0 0];

% generate message
load(SFile);  %生成信源比特
MsgLen = length(SendBit);

%% 请完成下述代码实现完整发射机
% convolutoinal coding
trel = poly2trellis(CoderConstraint, [171, 133]);
SendBitWithTail = [SendBit, zeros(size(1 : CoderConstraint - 1))];%  结尾处理, 在消息的结尾添加 coder_constraint-1 个零
code = convenc(SendBitWithTail, trel);%  调用库函数所生成卷积码

% add preamble 
data=[Preamble,code];

% FSK modulation



% 确保信号长度是SigLen
if length(SendSig)>SigLen
    SendSig = SendSig(1:SigLen);
elseif length(SendSig)<SigLen
    SendSig = [SendSig zeros(1,SigLen-length(SendSig))];
end

