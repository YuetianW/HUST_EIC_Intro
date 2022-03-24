
[x,fs]=audioread('SunshineSquare.wav');


x=x(:,1);
FS=length(x);
X=fft(x);
t=(0:FS-1)/fs;
figure(1)

subplot(2,1,1);plot(t,x);
title('原始语音信号时域波形');
xlabel('时间');
ylabel('赋值');
grid on;

subplot(2,1,2);plot(abs(X));
title('原始语音信号频谱');
xlabel('频率');
ylabel('幅度');
axis([0 1000000 0 8]);
grid on;

Fp1=1200;
Fp2=3000;
Fs1=1000;
Fs2=3200;
Ft=8000;
As=100;
Ap=1;
wp=[2*pi*Fp1/Ft,2*pi*Fp2/Ft];
ws=[2*pi*Fs1/Ft,2*pi*Fs2/Ft];
[n,wn]=ellipord(wp,ws,Ap,As,'s');
[b,a]=ellip(n,Ap,As,wn,'s');
[B,A]=bilinear(b,a,1);
[h,w]=freqz(B,A);
figure(6);
plot(w*Ft/pi/2,abs(h));
title('IIR带通滤波器');
xlabel('频率');
ylabel('幅度');
grid on;


x=x(:,1);
Y=fft(x);
y=filter(B,A,x);
Y1=fft(y);
n=0:length(x)-1;
t=(0:FS-1)/fs;
figure(7);
subplot(3,1,1);plot(t,y);grid on;
title('IIR带通滤波器滤波后语音信号时域波形');
xlabel('时间');
ylabel('赋值');
subplot(3,1,2);plot(n,abs(Y));grid on;
title('滤波前语音信号频谱');
xlabel('频率');
ylabel('幅度');
axis([0 1000000 0 5]);
subplot(3,1,3);plot(n,abs(Y1));grid on;
title('滤波后语音信号频谱');
xlabel('频率');
ylabel('幅度');
axis([0 1000000 0 5]);

a
