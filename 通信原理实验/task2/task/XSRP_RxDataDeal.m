%20171218，李玮修改可用

function [rxdataI,rxdataQ]=XSRP_RxDataDeal(udp_data_rr0,freqDiv,dataByteNumb)

%freqDiv==0，6个字节含2个I和2个Q
if(freqDiv==0)
	for m=1:dataByteNumb/3 
        %重新排列接收数据
        udp_data_ri(m) = udp_data_rr0(m*3-2)*16 + fix((udp_data_rr0(m*3-1))/16);
        temp=udp_data_rr0(m*3-1);
        udp_data_rq(m) = (mod(temp,16)) * 256 + udp_data_rr0(m*3);
        %负数的处理
        if(udp_data_ri(m)>=2049)
            udp_data_ri(m) = udp_data_ri(m)-4096;
        end
        if(udp_data_rq(m)>=2049)
            udp_data_rq(m) = udp_data_rq(m)-4096;
        end
%         udp_data_ri(m)= udp_data_ri(m)/52144;       %？
%         udp_data_rq(m)= udp_data_rq(m)/52144;       %？
    end
%freqDiv==0，4个字节含1个I和1个Q
else		
	for m=1:dataByteNumb/4
        %重新排列接收数据
		udp_data_ri(m) = udp_data_rr0(m*4-3) * 256 + udp_data_rr0(m*4-2);
        udp_data_rq(m) = udp_data_rr0(m*4-1) * 256 + udp_data_rr0(m*4);
        %负数的处理
        if(udp_data_ri(m)>=2049)
            udp_data_ri(m) = udp_data_ri(m)-4096;
        end
        if(udp_data_rq(m)>=2049)
            udp_data_rq(m) = udp_data_rq(m)-4096;
        end
%         udp_data_ri(m)= udp_data_ri(m)/52144;       %？
%         udp_data_rq(m)= udp_data_rq(m)/52144;       %？
	end
end

if(udp_data_ri(m)>2047)
 	udp_data_ri(m) = udp_data_ri(m)-4096;
end

if(udp_data_rq(m)>2047)
      	udp_data_rq(m) = udp_data_rq(m)-4096;
end

udp_data_ri(m)= udp_data_ri(m)/2047;
udp_data_rq(m)= udp_data_rq(m)/2047;

rxdataI = udp_data_ri;               %重组后的I路数据
rxdataQ = udp_data_rq;		%重组后的Q路数据
end


