---------------------------------------------
-- biu-fifo2dma-VF
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity biu_fifo2dma_VF is
port(reset :in  std_logic;
     fain:   in  std_logic;
     dackn:  in  std_logic;
     cntgt1: in  std_logic;
     ok:     in  std_logic;
     dreq:   out std_logic;
     frout:  out std_logic);
end biu_fifo2dma_VF;

---------------------------------------------

architecture struct of biu_fifo2dma_VF is

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

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p13: std_logic;
signal Ai_p13: std_logic;
signal Ro_p13: std_logic;
signal Ao_p13: std_logic;

signal dreq_set:   std_logic;
signal dreq_reset: std_logic;

signal frout_set:   std_logic;
signal frout_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p13: control_cell port map (Ri_p13, Ai_p13, Ro_p13, Ao_p13);

dreq_cell: output_cell port map (dreq_set, dreq_reset, dreq);
frout_cell: output_cell port map (frout_set, frout_reset, frout);

Ri_p2 <= not (ok and (Ro_p1));
Ri_p6 <= not (cntgt1 and not dackn and (Ro_p4 or Ro_p10));
Ri_p1 <= not (reset or (not ok and not fain and dackn and (Ro_p13));
Ri_p4 <= not (fain and (Ro_p2));
Ri_p8 <= not (not fain and dackn and (Ro_p6));
Ri_p10 <= not (fain and (Ro_p8));
Ri_p13 <= not (not cntgt1 and not dackn and (Ro_p4 or Ro_p10));


Ai_p2 <= not reset and (Ao_p4);
Ai_p6 <= not reset and (Ao_p8);
Ai_p1 <= (Ao_p2);
Ai_p4 <= not reset and (Ao_p13 and Ao_p6);
Ai_p8 <= not reset and (Ao_p10);
Ai_p10 <= not reset and (Ao_p13 and Ao_p6);
Ai_p13 <= not reset and (Ao_p1);


dreq_set <= not((Ro_p10) or (Ro_p4)) or not dreq_reset;
dreq_reset <= not reset and (not((Ro_p6) or (Ro_p13)));

frout_set <= not((Ro_p2) or (Ro_p8)) or not frout_reset;
frout_reset <= not reset and (not((Ro_p10) or (Ro_p4)));

end struct;
