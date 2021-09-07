`define MASK '1
module Filter_0 #(
  parameter PIXEL_SIZE = 3, // in bit
  parameter PIXEL_NUM  = 3)
(
  input  logic                     areset,
  input  logic                     clk, 
  input  logic [2**PIXEL_SIZE-1:0] mode,  
  input  logic [2**PIXEL_SIZE-1:0] omega, 
  input  logic [2**PIXEL_SIZE-1:0] epsilon, 
  input  logic [2**PIXEL_SIZE-1:0] pixel  [PIXEL_NUM], 
  output logic [2**PIXEL_SIZE-1:0] result [PIXEL_NUM],  
  input  logic                     clear,
  input  logic                     enable,   
  output logic                     ready);
  
  logic  [2**PIXEL_SIZE-1:0] Round;

  typedef enum {
    _IDLE_,
    _ROUND_
  } fsm; fsm state;

  always @(posedge clk or negedge areset)
    if (~areset) begin ready <= '0;
      for (int i=0; i<PIXEL_NUM; i++) 
        {Round,result[i]} <= '0; end    
    else case (state)
      _IDLE_: begin
        Round <= '0;
        ready <= '0;
        if (enable) begin 
          state <= _ROUND_;
          for (int i=0;i < PIXEL_NUM; i++) 
            result[i] <= '0; 
      end end
      _ROUND_: if (~clear) begin 
        Round <= Round+1; ready <= '1;       
        for (int i=0; i < PIXEL_NUM; i++) begin
          if ((pixel[i] > omega) && 
              (pixel[i] < epsilon)) 
                case (mode) 
                  0: result[i] <=`MASK;
                  1: result[i] <= Round;
                  2: result[i] <= pixel[i];
                  3: result[i] <= Round*PIXEL_NUM+(PIXEL_NUM-i-1);  
                //4: ____________________________________________
              endcase
          else result[i] <= '0;          
      end end 
      else state <= _IDLE_;
    endcase
          
endmodule

