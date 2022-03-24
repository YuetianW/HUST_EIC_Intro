function plot_function(y,fs,style)
    %style = 1时画频域图；style = 2 时画时域图
    nfft= 2^nextpow2(length(y));%找出大于y的个数的最大的2的指数值（自动进算最佳FFT步长nfft）
    y_ft=fft(y,nfft);%对y信号进行FFT，得到频率的幅值分布
    y_f=fs*(0:nfft/2-1)/nfft;%变换后对应的频率的序列
    if style==1        
       plot(y_f,2*abs(y_ft(1:nfft/2))/length(y));
       ylabel('幅值');xlabel('频率/Hz');title('信号频域谱');
    elseif style==2
        n=1:length(y);
        plot(n/fs,y);
        ylabel('幅值');xlabel('时间/s');title('信号时域谱');
    end
end