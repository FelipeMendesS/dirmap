---------------------------------------------
-- testFile2
-- by Felipe Mendes dos Santos, 03/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity testFile2 is
port(empty:        in  std_logic;
     startdmasend: in  std_logic;
     dack:         in  std_logic;
     done:         in  std_logic;
     dtc:          in  std_logic;
     ackin:        in  std_logic;
     ready:        out std_logic;
     endmaint:     out std_logic;
     regout:       out std_logic;
     dreq:         out std_logic;
);
end testFile2;

---------------------------------------------

architecture struct of testFile2 is

component control_cell is
port(Ri: in    std_logic;
     Ai: in    std_logic;
     Ro: inout std_logic;
     Ao: out   std_logic
);
end component;

component buffer_n is
generic(N: integer);
port(a: in  std_logic;
     b: out std_logic
);
end component;

component output_cell is
port(set:    in  std_logic;
     reset:  in  std_logic;
     output: out std_logic
);
end component;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p25: std_logic;
signal Ai_p25: std_logic;
signal Ro_p25: std_logic;
signal Ao_p25: std_logic;

signal Ri_p24: std_logic;
signal Ai_p24: std_logic;
signal Ro_p24: std_logic;
signal Ao_p24: std_logic;

signal Ri_p21: std_logic;
signal Ai_p21: std_logic;
signal Ro_p21: std_logic;
signal Ao_p21: std_logic;

signal Ri_p23: std_logic;
signal Ai_p23: std_logic;
signal Ro_p23: std_logic;
signal Ao_p23: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p17: std_logic;
signal Ai_p17: std_logic;
signal Ro_p17: std_logic;
signal Ao_p17: std_logic;

signal Ri_p19: std_logic;
signal Ai_p19: std_logic;
signal Ro_p19: std_logic;
signal Ao_p19: std_logic;

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

signal Ri_p15: std_logic;
signal Ai_p15: std_logic;
signal Ro_p15: std_logic;
signal Ao_p15: std_logic;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_Paux0: std_logic;
signal Ai_Paux0: std_logic;
signal Ro_Paux0: std_logic;
signal Ao_Paux0: std_logic;

signal Ro_p15_buffer: std_logic;

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal Ro_p23_buffer: std_logic;

signal ready_set:   std_logic
signal ready_reset: std_logic

signal endmaint_set:   std_logic
signal endmaint_reset: std_logic

signal regout_set:   std_logic
signal regout_reset: std_logic

signal dreq_set:   std_logic
signal dreq_reset: std_logic

begin

p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p25: control_cell port map (Ri_p25, Ai_p25, Ro_p25, Ao_p25);
p24: control_cell port map (Ri_p24, Ai_p24, Ro_p24, Ao_p24);
p21: control_cell port map (Ri_p21, Ai_p21, Ro_p21, Ao_p21);
p23: control_cell port map (Ri_p23, Ai_p23, Ro_p23, Ao_p23);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p17: control_cell port map (Ri_p17, Ai_p17, Ro_p17, Ao_p17);
p19: control_cell port map (Ri_p19, Ai_p19, Ro_p19, Ao_p19);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p15: control_cell port map (Ri_p15, Ai_p15, Ro_p15, Ao_p15);
p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);
buffer_1: buffer_n generic map(N => 8) port map (Ro_p15, Ro_p15_buffer);

Paux2: control_cell port map (Ri_Paux2, Ai_Paux2, Ro_Paux2, Ao_Paux2);
buffer_2: buffer_n generic map(N => 8) port map (Ro_p23, Ro_p23_buffer);

ready_cell: output_cell port map (ready_set, ready_reset, ready);
endmaint_cell: output_cell port map (endmaint_set, endmaint_reset, endmaint);
regout_cell: output_cell port map (regout_set, regout_reset, regout);
dreq_cell: output_cell port map (dreq_set, dreq_reset, dreq);

Ri_p1 <= not (reset or (Ro_p14))
Ri_p25 <= not (not done and dtc and (Ro_p24 and Ro_p6))
Ri_p24 <= not (empty and dack and not ackin and (Ro_p19 or Ro_Paux2))
Ri_p21 <= not (not empty and not ackin and (Ro_p19 or Ro_Paux2))
Ri_p23 <= not (ackin and (Ro_p21))
Ri_p10 <= not (not dack and not dtc and (Ro_p8))
Ri_p4 <= not (not startdmasend and (Ro_p2))
Ri_p8 <= not (done and dtc and (Ro_p24 and Ro_p6))
Ri_p12 <= not (ackin and (Ro_Paux1 or Ro_p10))
Ri_p17 <= not (not dack and not dtc and (Ro_p25))
Ri_p19 <= not (ackin and (Ro_p17))
Ri_p6 <= not (dack and (Ro_p4))
Ri_p15 <= not (not empty and not ackin and (Ro_p12))
Ri_p2 <= not (startdmasend and (Ro_p1))
Ri_p14 <= not (empty and not ackin and (Ro_p12))

Ri_Paux1 <= not Ro_p15_buffer;
Ri_Paux2 <= not Ro_p23_buffer;

Ai_p1 <= ((Ao_p2) or not (Ao_p14));
Ai_p25 <= not reset and ((Ao_p17) or not (Ao_p24 and Ao_p6));
Ai_p24 <= not reset and ((Ao_p25 and Ao_p8) or not (Ao_p19 and Ao_p23));
Ai_p21 <= not reset and ((Ao_p23) or not (Ao_p19 and Ao_p23));
Ai_p23 <= not reset and ((Ao_Paux2) or not (Ao_p21));
Ai_p10 <= not reset and ((Ao_p12) or not (Ao_p8));
Ai_p4 <= not reset and ((Ao_p6) or not (Ao_p2));
Ai_p8 <= not reset and ((Ao_p10) or not (Ao_p24 and Ao_p6));
Ai_p12 <= not reset and ((Ao_p14 and Ao_p15) or not (Ao_p15 and Ao_p10));
Ai_p17 <= not reset and ((Ao_p19) or not (Ao_p25));
Ai_p19 <= not reset and ((Ao_p21 and Ao_p24) or not (Ao_p17));
Ai_p6 <= not reset and ((Ao_p25 and Ao_p8) or not (Ao_p4));
Ai_p15 <= not reset and ((Ao_Paux1) or not (Ao_p12));
Ai_p2 <= not reset and ((Ao_p4) or not (Ao_p1));
Ai_p14 <= not reset and ((Ao_p1) or not (Ao_p12));

Ai_Paux1 <= not reset and ((Ao_p12) or not Ao_p15);
Ai_Paux2 <= not reset and ((Ao_p21 and Ao_p24) or not Ao_p23);

ready_set <= (not((Ro_p24 and Ro_p6)) or not ready_reset);
ready_reset <= not reset and (not((Ro_p8) or (Ro_p25)));

endmaint_set <= not reset and (not((Ro_p14)) or not endmaint_reset);
endmaint_reset <= not((Ro_p2)));

regout_set <= (not((Ro_p17) or (Ro_p10) or (Ro_p21) or (Ro_p15)) or not regout_reset);
regout_reset <= not reset and (not((Ro_p19) or (Ro_p12) or (Ro_p23)));

dreq_set <= (not((Ro_p4)) or not dreq_reset);
dreq_reset <= not reset and (not((Ro_p8)));

end struct;
