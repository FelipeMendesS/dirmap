---------------------------------------------
-- selmerge2ph-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity selmerge2ph_vf is
port(reset :in  std_logic;
     sel: in  std_logic;
     r2:  in  std_logic;
     r:   in  std_logic;
     s2:  out std_logic;
     a:   out std_logic);
end selmerge2ph_vf;

---------------------------------------------

architecture struct of selmerge2ph_vf is

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

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p16: std_logic;
signal Ai_p16: std_logic;
signal Ro_p16: std_logic;
signal Ao_p16: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p20: std_logic;
signal Ai_p20: std_logic;
signal Ro_p20: std_logic;
signal Ao_p20: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p19: std_logic;
signal Ai_p19: std_logic;
signal Ro_p19: std_logic;
signal Ao_p19: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p17: std_logic;
signal Ai_p17: std_logic;
signal Ro_p17: std_logic;
signal Ao_p17: std_logic;

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal s2_set:   std_logic;
signal s2_reset: std_logic;

signal a_set:   std_logic;
signal a_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p20: control_cell port map (Ri_p20, Ai_p20, Ro_p20, Ao_p20);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p19: control_cell port map (Ri_p19, Ai_p19, Ro_p19, Ao_p19);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p17: control_cell port map (Ri_p17, Ai_p17, Ro_p17, Ao_p17);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);

s2_cell: output_cell port map (s2_set, s2_reset, s2);
a_cell: output_cell port map (a_set, a_reset, a);

Ri_p2 <= not (not sel and r and (Ro_p1));
Ri_p6 <= not (not sel and not r and (Ro_p14 or Ro_p4));
Ri_p12 <= not (r2 and (Ro_p20));
Ri_p16 <= not (not r2 and (Ro_p19));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p10 or Ro_p8)));
Ri_p20 <= not (not sel and not r and (Ro_p16 or Ro_p17));
Ri_p4 <= not (r2 and (Ro_p2));
Ri_p18 <= not (sel and not r and (Ro_p14 or Ro_p4));
Ri_p14 <= not (sel and r and (Ro_p12 or Ro_Paux1));
Ri_p8 <= not (not r2 and (Ro_p6));
Ri_p19 <= not (not sel and r and (Ro_p12 or Ro_Paux1));
Ri_p10 <= not (sel and not r and (Ro_p16 or Ro_p17));
Ri_p17 <= not (sel and r and (Ro_p1));

Ri_Paux1 <= not (Ro_p18 and Ai_Paux1);

Ai_p2 <= not reset and (Ao_p4);
Ai_p6 <= not reset and (Ao_p8);
Ai_p12 <= not reset and (Ao_p14 and Ao_p19);
Ai_p16 <= not reset and (Ao_p10 and Ao_p20);
Ai_p1 <= (Ao_p2 and Ao_p17);
Ai_p20 <= not reset and (Ao_p12);
Ai_p4 <= not reset and (Ao_p18 and Ao_p6);
Ai_p18 <= not reset and (Ao_Paux1);
Ai_p14 <= not reset and (Ao_p18 and Ao_p6);
Ai_p8 <= not reset and (Ao_p1);
Ai_p19 <= not reset and (Ao_p16);
Ai_p10 <= not reset and (Ao_p1);
Ai_p17 <= not reset and (Ao_p10 and Ao_p20);

Ai_Paux1 <= not reset and (Ao_p14 and Ao_p19);

s2_set <= not((Ro_p2) or (Ro_p20)) or not s2_reset;
s2_reset <= not reset and (not((Ro_p19) or (Ro_p6)));

a_set <= not((Ro_p14) or (Ro_p16) or (Ro_p4) or (Ro_p17)) or not a_reset;
a_reset <= not reset and (not((Ro_p10) or (Ro_p8) or (Ro_p18) or (Ro_p12)));

end struct;
