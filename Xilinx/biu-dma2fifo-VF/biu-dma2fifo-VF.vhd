---------------------------------------------
-- biu-dma2fifo-VF
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity biu_dma2fifo_VF is
port(reset :in  std_logic;
     frin:   in  std_logic;
     dackn:  in  std_logic;
     cntgt1: in  std_logic;
     ok:     in  std_logic;
     faout:  out std_logic;
     dreq:   out std_logic);
end biu_dma2fifo_VF;

---------------------------------------------

architecture struct of biu_dma2fifo_VF is

component control_cell is
port(Ri: in    std_logic;
     Ai: in    std_logic;
     Ro: inout std_logic;
     Ao: out   std_logic
);
end component;

component output_cell is
port(set:    in  std_logic;
     reset:  in  std_logic;
     output: out std_logic
);
end component;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p16: std_logic;
signal Ai_p16: std_logic;
signal Ro_p16: std_logic;
signal Ao_p16: std_logic;

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p15: std_logic;
signal Ai_p15: std_logic;
signal Ro_p15: std_logic;
signal Ao_p15: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal faout_set:   std_logic;
signal faout_reset: std_logic;

signal dreq_set:   std_logic;
signal dreq_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p15: control_cell port map (Ri_p15, Ai_p15, Ro_p15, Ao_p15);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);

faout_cell: output_cell port map (faout_set, faout_reset, faout);
dreq_cell: output_cell port map (dreq_set, dreq_reset, dreq);

Ri_p2 <= not (ok and (Ro_p1));
Ri_p16 <= not (not cntgt1 and not dackn and (Ro_p2));
Ri_p12 <= not (frin and dackn and (Ro_p15 or Ro_p16));
Ri_p6 <= not (frin and dackn and (Ro_p10 or Ro_p4));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p14)));
Ri_p4 <= not (cntgt1 and not dackn and (Ro_p2));
Ri_p14 <= not (not ok and not frin and (Ro_p12));
Ri_p8 <= not (not frin and (Ro_p6));
Ri_p15 <= not (not cntgt1 and not dackn and (Ro_p8));
Ri_p10 <= not (cntgt1 and not dackn and (Ro_p8));


Ai_p2 <= not reset and (Ao_p4 and Ao_p16);
Ai_p16 <= not reset and (Ao_p12);
Ai_p12 <= not reset and (Ao_p14);
Ai_p6 <= not reset and (Ao_p8);
Ai_p1 <= (Ao_p2);
Ai_p4 <= not reset and (Ao_p6);
Ai_p14 <= not reset and (Ao_p1);
Ai_p8 <= not reset and (Ao_p10 and Ao_p15);
Ai_p15 <= not reset and (Ao_p12);
Ai_p10 <= not reset and (Ao_p6);


faout_set <= not((Ro_p6) or (Ro_p12)) or not faout_reset;
faout_reset <= not reset and (not((Ro_p14) or (Ro_p8)));

dreq_set <= not((Ro_p2) or (Ro_p8)) or not dreq_reset;
dreq_reset <= not reset and (not((Ro_p4) or (Ro_p16) or (Ro_p15) or (Ro_p10)));

end struct;
