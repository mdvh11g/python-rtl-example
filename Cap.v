
`define Filter_0

`include "../rtl/Filter_0.sv"

module Cap #(
  parameter SIZE = 3, // in bit
  parameter NUM  = 4)
(
 
  input  logic                   areset,
  input  logic                   clk,    
  input  logic             [1:0] mode,          
  input  logic [NUM*2**SIZE-1:0] flow,  
  output logic [NUM*2**SIZE-1:0] result, 
  input  logic     [2**SIZE-1:0] omega, 
  input  logic     [2**SIZE-1:0] epsilon, 
  input  logic                   clear,      
  input  logic                   enable,   
  output logic                   ready);
  
  logic [2**SIZE-1:0] pp [NUM];
  logic [2**SIZE-1:0] rr [NUM];

  for (genvar i=0; i<NUM;i++) begin
    assign pp[i] = flow[(i+1)*2**SIZE-1:i*2**SIZE];
    assign result[(i+1)*2**SIZE-1:i*2**SIZE] = rr[NUM-i-1];
  end    

`ifdef Filter_0
    
  Filter_0 #(SIZE,NUM)
  Round (
    .areset(areset),
    .clk(clk), 
    .pixel(pp),  
    .result(rr),  
    .mode(mode),
    .omega(omega),
    .epsilon(epsilon),
    .clear(clear),
    .enable(enable),   
    .ready(ready)); 
    
`endif   
         

`ifdef Filter_1



`endif 


        
endmodule



