
[audio_data,fs]=audioread('SunshineSquare.wav');
% Y = fft(y);
% % totalSamples = length(Y);
% Yp = abs(Y);
% % L = floor(fs/2)+1;
% % Yh = Y(1:L);
% % h = Yh/fs;
% % fz = fs/totalSamples;
% % k = 0:L-1;
% % f = fz*k;
% L = floor(fs/2)+1;
% plot(Yp);
f=fftshift(fft(audio_data));                  %b表示信号值data
w=linspace(-floor(fs)/2,floor(fs)/2,length(audio_data));  %根据奈奎斯特采样定理，512/2为最大频率
figure1;
f1 = plot(w,abs(f));                      %Hz为单位

Fs=fs;
wp=[0.08*2*pi/Fs,0.2*2*pi/Fs];                %设置通带数字角频率
ws=[0.10*2*pi/Fs,0.18*2*pi/Fs];  

Rp=1;                                   %设置通带波纹系数
Rs=20;                                  %设置阻带波纹系数     

[N,Wn]=buttord(wp,ws,Rp,Rs,'s');        %求巴特沃斯滤波器阶数N和截止频率Wn
fprintf('巴特沃斯滤波器 N= %4d\n',N);    %显示滤波器阶数
[bb,ab]=butter(N,Wn,'s');               %求巴特沃斯滤波器系数，即求传输函数的分子和分母的系数向量
b2=filter(bb,ab,audio_data);    


%观察响应
W=-600:0.1:600;                             %设置模拟频率
[Hb,wb]=freqz(bb,ab,W,Fs);                  %求巴特沃斯滤波器频率响应
f2 = plot(wb,20*log10(abs(Hb)),'b');             %作图
xlabel('Hz');
ylabel('幅值/dB');

f1=fft(b2);                            %b2是滤波后信号
w1=linspace(-floor(fs)/2,floor(fs)/2,length(b2));  %根据奈奎斯特采样定理，512/2为最大频率
f3 = plot(w1,abs(f1));
