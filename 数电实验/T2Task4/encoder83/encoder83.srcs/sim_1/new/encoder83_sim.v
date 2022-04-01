`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/09/09 17:54:19
// Design Name: 
// Module Name: encoder83_sim
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module encoder83_sim(

    );
    reg [7:0] I;
    wire [2:0] Y;
    encoder83 encoder_u0(I,Y);
       initial begin
       I = 8'h00;
       #10;
       I = 8'b00000001;
       #10;
       I = 8'b0000001x;
       #10;
       I = 8'b000001xx;
       #10;
       I = 8'b00001xxx;
       #10;       
       I = 8'b0001xxxx;
       #10;
       I = 8'b001xxxxx;
       #10;       
       I = 8'b01xxxxxx;
       #10;      
       I = 8'b1xxxxxxx;
       #10;  
       $stop;    
             
    end
                     
    
    
endmodule
