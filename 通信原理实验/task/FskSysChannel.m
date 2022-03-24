%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  FileName:            FskSysChannel.m
%  Description:         信道
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Parameter List:       
%       Output Parameter
%           RecvSig         接收信号
%           ChanParameter   信道参数
%       Input Parameter
%           SendSig     发射信号
%           Fs          采样率
%           Amax        最大信号幅度
%           Pmax        最大相位偏移
%           Fmax        最大频偏 Hz
%           Tmax        最大时间偏移 秒
%           SNR         信噪比
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [ RecvSig, ChannelParameter] = FskSysChannel(SendSig,Fs,Amax,Pmax,Fmax,Tmax,SNR)

% 具体幅度
A = (0.1+0.9*rand(1,1))*Amax;
% 具体相偏
P = (2*rand(1,1)-1)*Pmax;
% 具体频偏
F = (2*rand(1,1)-1)*Fmax;
% 具体时偏
T = floor(rand(1,1)*Tmax*Fs);

ChannelParameter = [ A P F T SNR];

% 加时偏
SendSig = [ zeros(1,T) SendSig(1,1:end-T) ];

% 加频偏、相偏和幅度变化
t = (0:length(SendSig)-1)/Fs;
RecvSig = A*exp(j*(2*pi*F*t+P)).*SendSig; 

RecvSig = awgn(RecvSig, SNR, 'measured');%加高斯白噪声
