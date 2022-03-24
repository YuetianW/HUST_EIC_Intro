function [rxdataIQ] = XSRP_RFLoopback(txdataIQ)

%%对数据长度进行补零或溢出删除
SAMPLE_LENGTH = 30720;                  % 样点数30.72Msps * 1ms
TxdataI=zeros(1,SAMPLE_LENGTH);
TxdataQ=zeros(1,SAMPLE_LENGTH);
if length(txdataIQ)>=SAMPLE_LENGTH
    TxdataI=real(txdataIQ(1,1:SAMPLE_LENGTH));
    TxdataQ=imag(txdataIQ(1,1:SAMPLE_LENGTH));
else 
    TxdataI(1,1:length(txdataIQ))=real(txdataIQ);
    TxdataQ(1,1:length(txdataIQ))=imag(txdataIQ);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%发送数据处理
%放大峰值，浮点取整
len = SAMPLE_LENGTH*2;
dataIQ = zeros(1,len);
dataIQ(1,1:2:len-1) = TxdataI(1,:);
dataIQ(1,2:2:len) = TxdataQ(1,:);
dataIQ = dataIQ.*(2047/max(dataIQ));    %放大峰值至2000,接近理论峰值2047
dataIQ = fix(dataIQ);                   %浮点数强制取整

%防止溢出，并对负数进行补码操作
for n = 1 : len
    if dataIQ(n) > 2047
      dataIQ(n) = 2047;
    elseif  dataIQ(n) < 0
      dataIQ(n) = 4096 + dataIQ(n);
    end
end

%按接口定义排列比特序
dataIQ(1,1:2:len-1) = dataIQ(1,1:2:len).*16;    %I路：b11~b0 空4bits
dataIQ(1,2:2:len) = fix(dataIQ(1,2:2:len)./256) + rem(dataIQ(1,2:2:len),256).*256;  %Q路：b7~b0 空4bits b11~b8
dataIQ = uint16(dataIQ);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%定义配置参数常量
test_set_sync_clock = uint8(hex2dec({'00','00','99','bb',  '69','00','00','00',  '00','00','00','00',  '00','00','00','00',  '00','00','00','00'}));%OK
test_Set_router = uint8(hex2dec({'00','00','99','bb', '68','00','00','00',  '00','06','00','00',  '00','00','00','00',  '00','00','00','00'}));%网口环回%OK
test_set_delay_system = uint8(hex2dec({'00','00','99','bb', '67','00','00','00',  '00','00','00','00',  '00','00','00','00',  '00','00','00','00'}));
test_tx_command = uint8(hex2dec({'00','00','99','bb', '65','02','00','03',  '00','01','78','00',  '00','00','00','00',  '00','00','00','00'}));%0A  10个时隙，03FF 时隙开关000001111111111，0000 分频，7800 数据个数/时隙30720%OK
%test_tx_command = uint8(hex2dec({'00','00','99','bb', '65','0A','03','FF',  '00','03','78','00',  '00','00','00','00',  '00','00','00','00'}));%0A  10个时隙，03FF 时隙开关000001111111111，0000 分频，7800 数据个数/时隙30720
test_Send_IQ = uint8(hex2dec({'00','00','99','bb', '64','00','00','00',  '00','00','00','00',  '00','00','00','00',  '00','00','00','00'}));
test_Get_IQ  = uint8(hex2dec({'00','00','99','bb', '66','01','00','01',  '00','80','00','F0',  '00','00','00','00',  '00','00','00','00'}));%01 采集时隙号，0000 分频，0060 包的数量96，00F0 包的大小240（实际接收字节数为配置值乘以4）%OK
%test_Get_IQ  = uint8(hex2dec({'00','00','99','bb', '66','01','00','03',  '00','60','00','F0',  '00','00','00','00',  '00','00','00','00'}));%01 采集时隙号，0000 分频，0060 包的数量96，00F0 包的大小240（实际接收字节数为配置值乘以4）
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%创建UDP对象，并打开
udp_obj = udp('192.168.1.166',13345,'LocalHost','192.168.1.180','LocalPort',12345,'TimeOut',3,'OutputBufferSize',61440,'InputBufferSize',61440*10);
udp_obj.Timeout=3;
fopen(udp_obj);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%发送配置命令
fwrite(udp_obj, test_set_sync_clock, 'uint8');
fwrite(udp_obj, test_Set_router,  'uint8');
fwrite(udp_obj, test_set_delay_system, 'uint8');
fwrite(udp_obj, test_tx_command, 'uint8');
fwrite(udp_obj, test_Send_IQ, 'uint8');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%发送已调数据
SEND_PACKET_LENGTH = 512;   %发送UDP包长度，数据为U16，所以每个UDP包发送字节数数为512*2，
for pn = 1:fix(SAMPLE_LENGTH*2/SEND_PACKET_LENGTH)
    fwrite(udp_obj, dataIQ(1,((pn-1)*SEND_PACKET_LENGTH+1) : (pn*SEND_PACKET_LENGTH)), 'uint16');
end      
%fwrite(udp_obj, dataIQ(1,(pn*SEND_PACKET_LENGTH+1 ): (SAMPLE_LENGTH*2)),'uint16');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%发送采集（接收）数据启动命令
fwrite(udp_obj, test_Get_IQ, 'uint8');

%% 采集变量初始化
RECV_PACKET_LENGTH = 240*4;                         %接收包字节数。大小为配置值乘以4。
data_byte_numb = SAMPLE_LENGTH*4;                   %接收数据字节数，0分频1个IQ样点对应3个字节
udp_data_ri = zeros(1, SAMPLE_LENGTH);        
udp_data_rq = zeros(1, SAMPLE_LENGTH);
udp_data_rr0 = zeros(1, SAMPLE_LENGTH*4);
rxdataI = zeros(1,SAMPLE_LENGTH);
rxdataQ = zeros(1,SAMPLE_LENGTH);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%开始接收数据
recvInd = 1;
data_byte_c = 0;
while recvInd == 1    
    % 从网口读数据
    [udp_data,count] = fread(udp_obj,RECV_PACKET_LENGTH);
    
    %接收数据拼接
    for (pj = 1 : count)
        udp_data_rr0(data_byte_c+pj) = udp_data(pj);
    end
    data_byte_c = data_byte_c + count;
    %判断接收总字节数
    if (data_byte_c>=data_byte_numb)         %如果数据接收完成或超时没有接收到数据则退出            
        recvInd = 0;    % 停止运行
        break
    end
    if count == 0 
        disp('UDP接收数据超时退出') 
        recvInd = 0;    % 停止运行
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%关闭UDP对象
fclose(udp_obj);
delete(udp_obj);
clear udp_obj;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%接收数据处理
freqDiv=1;
 [rxdataI,rxdataQ]=XSRP_RxDataDeal(udp_data_rr0,freqDiv,data_byte_numb);

rxdataIQ=rxdataI+rxdataQ*i;
rxdataIQ=rxdataIQ/2047;
%plot(rxdataI)
end