function y=Chebyshev_bandstop_filter(x,fplowow,fphighigh,fplow,fphigh,rp,rs,Fs)
    %实现切比雪夫带阻滤波器
    %x:需要带通滤波的序列
    % fplowow：阻带左边界
    % fphighigh：阻带右边界
    % fplow：衰减截止左边界
    % fphigh：衰变截止右边界
    %rp：边带区衰减DB数设置
    %rs：截止区衰减DB数设置
    %FS：序列x的采样频率
    
    wp1=2*pi*fplowow/Fs;
    wp3=2*pi*fphighigh/Fs;
    wsl=2*pi*fplow/Fs;
    wsh=2*pi*fphigh/Fs;
    wp=[wp1 wp3];
    ws=[wsl wsh];
    % 使用MATLAB切比雪夫滤波器函数；
    [n,wn]=cheb1ord(ws/pi,wp/pi,rp,rs);
    [bz1,az1]=cheby1(n,rp,wp/pi,'stop');
    %绘制滤波器的幅度响应
    [h,w]=freqz(bz1,az1,256,Fs);
    h=20*log10(abs(h));
    figure;plot(w,h);
    ylabel('衰减/dB');xlabel('频率/Hz');title('滤波器幅度响应');grid on;
    %滤波
    y=filter(bz1,az1,x);
end




