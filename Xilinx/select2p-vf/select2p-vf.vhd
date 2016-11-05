---------------------------------------------
-- select2p-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity select2p_vf is
port(reset :in  std_logic;
     sel: in  std_logic;
     r:   in  std_logic;
     s2:  out std_logic;
     a:   out std_logic);
end select2p_vf;

---------------------------------------------

architecture struct of select2p_vf is

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

signal Ri_p16: std_logic;
signal Ai_p16: std_logic;
signal Ro_p16: std_logic;
signal Ao_p16: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p15: std_logic;
signal Ai_p15: std_logic;
signal Ro_p15: std_logic;
signal Ao_p15: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

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

signal Ri_Paux2: std_logic;
signal Ai_Paux2: std_logic;
signal Ro_Paux2: std_logic;
signal Ao_Paux2: std_logic;

signal s2_set:   std_logic;
signal s2_reset: std_logic;

signal a_set:   std_logic;
signal a_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p15: control_cell port map (Ri_p15, Ai_p15, Ro_p15, Ao_p15);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p17: control_cell port map (Ri_p17, Ai_p17, Ro_p17, Ao_p17);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);

Paux2: control_cell port map (Ri_Paux2, Ai_Paux2, Ro_Paux2, Ao_Paux2);

s2_cell: output_cell port map (s2_set, s2_reset, s2);
a_cell: output_cell port map (a_set, a_reset, a);

Ri_p2 <= not (sel and r and (Ro_p1));
Ri_p6 <= not (sel and not r and (Ro_p16 or Ro_p14));
Ri_p16 <= not (not sel and r and (Ro_p1));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p17 or Ro_p10)));
Ri_p18 <= not (not sel and r and (Ro_Paux2 or Ro_p15));
Ri_p15 <= not (not sel and not r and (Ro_p2 or Ro_Paux1));
Ri_p14 <= not (sel and r and (Ro_Paux2 or Ro_p15));
Ri_p10 <= not (sel and not r and (Ro_p2 or Ro_Paux1));
Ri_p17 <= not (not sel and not r and (Ro_p16 or Ro_p14));

Ri_Paux1 <= not (Ro_p18 and Ai_Paux1);
Ri_Paux2 <= not (Ro_p6 and Ai_Paux2);

Ai_p2 <= not reset and (Ao_p10 and Ao_p15);
Ai_p6 <= not reset and (Ao_Paux2);
Ai_p16 <= not reset and (Ao_p6 and Ao_p17);
Ai_p1 <= (Ao_p2 and Ao_p16);
Ai_p18 <= not reset and (Ao_Paux1);
Ai_p15 <= not reset and (Ao_p18 and Ao_p14);
Ai_p14 <= not reset and (Ao_p6 and Ao_p17);
Ai_p10 <= not reset and (Ao_p1);
Ai_p17 <= not reset and (Ao_p1);

Ai_Paux1 <= not reset and (Ao_p10 and Ao_p15);
Ai_Paux2 <= not reset and (Ao_p18 and Ao_p14);

s2_set <= not((Ro_p16) or (Ro_p15)) or not s2_reset;
s2_reset <= not reset and (not((Ro_p18) or (Ro_p17)));

a_set <= not((Ro_p2) or (Ro_Paux2)) or not a_reset;
a_reset <= not reset and (not((Ro_p14) or (Ro_p10)));

end struct;
