%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  FileName:            FskSysRx.m
%  Description:         FSK系统接收机
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Parameter List:       
%       Output Parameter
%           RecvFskDemod        FSK解调信号
%           RecvCorr            同步码相关结果
%           RecvSymbolSampled   码元抽样
%           RecvBit             接收到的比特
%       Input Parameter
%           Fs          采样率
%           Rs          码元速率
%           MsgLen      比特数据源长度
%           RecvSig     接收信号

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [RecvFskDemod,RecvCorr,RecvSymbolSampled,RecvBit] = FskSysRx(Fs,Rs,MsgLen,RecvSig)
UpSampleRate=Fs/Rs;
Ts=UpSampleRate; % symbol period
SymbolLen = (MsgLen+6)*2;
CoderConstraint = 7;%  约束长度 
Preamble=[1 1 1 1 0 1 0 1 1 0 0 1 0 0 0 0];
PreambleSig=[-1 -1 -1 -1 +1 -1 +1 -1 -1 +1 +1 -1 +1 +1 +1 +1];
PreambleLen = 16;

%% 请完成下述代码实现完整接收机
% filter design


% filtering of carrier1


% filtering of carrier2


% FSK demodulation


% preamble search


% sampled symbol


% convolutoinal decoding


end
    

