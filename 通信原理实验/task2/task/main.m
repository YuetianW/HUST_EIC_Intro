close all

run_type = 0;           % 仿真还是设备运行

%% 系统参数
Fs = 200e3;           % 系统采样率
Rs = 10e3;                 % 码元速率
SFile = 'C:\Users\admin\Desktop\USRP0902\DpskSys_0910\SendBit.mat'; %读取数据文件
SigLen = 200e3;        % 信号采样点数，对应时间长度为1秒

%% 信道参数
Amax = 1;               % 最大信号幅度
Pmax = pi;              % 最大相位偏差
Fmax = 512/4;           % 最大频偏，单位Hz
Tmax = 0.005;           % 最大时偏，单位秒
SNR = -3;                % 信噪比

%% 发射机
[SendBit,SendSig,MsgLen]  = FskSysTx(Fs, Rs, SFile, SigLen);


%% 信道
if run_type==0
    [RecvSig, ChannelParameter ] = FskSysChannel(SendSig,Fs,Amax,Pmax,Fmax,Tmax,SNR);
else
    [RecvSig] = XSRP_RFLoopback(SendSig);
end

%% 接收机
[RecvFskDemod,RecvCorr,RecvSymbolSampled,RecvBit] = FskSysRx(Fs,Rs,MsgLen,RecvSig);


%% 误码统计
ErrNum = sum(xor(SendBit(1,1:end-1),RecvBit(1,1:end-1)));

%% 波形打印
% 以下数据或者打印或者画波形
figure;plot(SendBit);title('SendBit：数据源比特');
figure;plot(phase(SendSig));title('phase(SendSig)：FSK发送信号相位');
figure;plot(real(RecvSig));title('real(RecvSig)：FSK接收信号');
figure;plot(real(RecvFskDemod));title('real(RecvFskDemod)：FSK解调后信号');
figure;plot(RecvCorr);title('RecvCorr：preamble相关结果');
figure;plot(real(RecvSymbolSampled));title('real(RecvSymbolSampled)：抽样码元');
figure;plot(RecvBit);title('RecvBit：译码比特');
figure;plot(abs(RecvBit-SendBit));title('abs(RecvBit-SendBit)：接收发送比特错误');

ChannelParameter  % 打印信道参数
ErrNum  % 打印错误比特数



