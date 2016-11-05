---------------------------------------------
-- des-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity des_vf is
port(reset :in  std_logic;
     my:    in  std_logic;
     Es1:   in  std_logic;
     Es0:   in  std_logic;
     Es2:   in  std_logic;
     start: in  std_logic;
     s1:    out std_logic;
     MA1:   out std_logic;
     s2:    out std_logic;
     done:  out std_logic;
     s0:    out std_logic;
     MM1:   out std_logic;
     k:     out std_logic);
end des_vf;

---------------------------------------------

architecture struct of des_vf is

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

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p15: std_logic;
signal Ai_p15: std_logic;
signal Ro_p15: std_logic;
signal Ao_p15: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal s1_set:   std_logic;
signal s1_reset: std_logic;

signal MA1_set:   std_logic;
signal MA1_reset: std_logic;

signal s2_set:   std_logic;
signal s2_reset: std_logic;

signal done_set:   std_logic;
signal done_reset: std_logic;

signal s0_set:   std_logic;
signal s0_reset: std_logic;

signal MM1_set:   std_logic;
signal MM1_reset: std_logic;

signal k_set:   std_logic;
signal k_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p15: control_cell port map (Ri_p15, Ai_p15, Ro_p15, Ao_p15);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);

s1_cell: output_cell port map (s1_set, s1_reset, s1);
MA1_cell: output_cell port map (MA1_set, MA1_reset, MA1);
s2_cell: output_cell port map (s2_set, s2_reset, s2);
done_cell: output_cell port map (done_set, done_reset, done);
s0_cell: output_cell port map (s0_set, s0_reset, s0);
MM1_cell: output_cell port map (MM1_set, MM1_reset, MM1);
k_cell: output_cell port map (k_set, k_reset, k);

Ri_p2 <= not (start and (Ro_p1));
Ri_p6 <= not (not my and Es2 and (Ro_p12 or Ro_p4));
Ri_p12 <= not (not Es1 and (Ro_p10));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p14)));
Ri_p4 <= not (Es0 and (Ro_p2));
Ri_p8 <= not (Es1 and (Ro_p6));
Ri_p14 <= not (not start and not Es0 and not Es2 and (Ro_p15));
Ri_p15 <= not (my and Es2 and (Ro_p12 or Ro_p4));
Ri_p10 <= not (not Es2 and (Ro_p8));


Ai_p2 <= not reset and (Ao_p4);
Ai_p6 <= not reset and (Ao_p8);
Ai_p12 <= not reset and (Ao_p15 and Ao_p6);
Ai_p1 <= (Ao_p2);
Ai_p4 <= not reset and (Ao_p15 and Ao_p6);
Ai_p8 <= not reset and (Ao_p10);
Ai_p14 <= not reset and (Ao_p1);
Ai_p15 <= not reset and (Ao_p14);
Ai_p10 <= not reset and (Ao_p12);


s1_set <= not((Ro_p6)) or not s1_reset;
s1_reset <= not reset and (not((Ro_p10)));

MA1_set <= not((Ro_p6)) or not MA1_reset;
MA1_reset <= not reset and (not((Ro_p12)));

s2_set <= not((Ro_p4) or (Ro_p12)) or not s2_reset;
s2_reset <= not reset and (not((Ro_p8) or (Ro_p15)));

done_set <= not reset and (not((Ro_p14)) or not done_reset;
done_reset <= not((Ro_p2)));

s0_set <= not((Ro_p2)) or not s0_reset;
s0_reset <= not reset and (not((Ro_p15)));

MM1_set <= not((Ro_p4) or (Ro_p12)) or not MM1_reset;
MM1_reset <= not reset and (not((Ro_p8) or (Ro_p14)));

k_set <= not((Ro_p6)) or not k_reset;
k_reset <= not reset and (not((Ro_p12)));

end struct;
