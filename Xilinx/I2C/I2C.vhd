---------------------------------------------
-- I2C
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity I2C is
port(reset :in  std_logic;
     aux: in  std_logic;
     CLK: in  std_logic;
     SDA: in  std_logic;
     a:   out std_logic;
     b:   out std_logic);
end I2C;

---------------------------------------------

architecture struct of I2C is

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

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p7: std_logic;
signal Ai_p7: std_logic;
signal Ro_p7: std_logic;
signal Ao_p7: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p15: std_logic;
signal Ai_p15: std_logic;
signal Ro_p15: std_logic;
signal Ao_p15: std_logic;

signal Ri_p19: std_logic;
signal Ai_p19: std_logic;
signal Ro_p19: std_logic;
signal Ao_p19: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p3: std_logic;
signal Ai_p3: std_logic;
signal Ro_p3: std_logic;
signal Ao_p3: std_logic;

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p5: std_logic;
signal Ai_p5: std_logic;
signal Ro_p5: std_logic;
signal Ao_p5: std_logic;

signal Ri_p16: std_logic;
signal Ai_p16: std_logic;
signal Ro_p16: std_logic;
signal Ao_p16: std_logic;

signal Ri_p11: std_logic;
signal Ai_p11: std_logic;
signal Ro_p11: std_logic;
signal Ao_p11: std_logic;

signal Ri_p9: std_logic;
signal Ai_p9: std_logic;
signal Ro_p9: std_logic;
signal Ao_p9: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal a_set:   std_logic;
signal a_reset: std_logic;

signal b_set:   std_logic;
signal b_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p7: control_cell port map (Ri_p7, Ai_p7, Ro_p7, Ao_p7);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p15: control_cell port map (Ri_p15, Ai_p15, Ro_p15, Ao_p15);
p19: control_cell port map (Ri_p19, Ai_p19, Ro_p19, Ao_p19);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p3: control_cell port map (Ri_p3, Ai_p3, Ro_p3, Ao_p3);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p5: control_cell port map (Ri_p5, Ai_p5, Ro_p5, Ao_p5);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p11: control_cell port map (Ri_p11, Ai_p11, Ro_p11, Ao_p11);
p9: control_cell port map (Ri_p9, Ai_p9, Ro_p9, Ao_p9);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);

a_cell: output_cell port map (a_set, a_reset, a);
b_cell: output_cell port map (b_set, b_reset, b);

Ri_p2 <= not (SDA and CLK and (Ro_p1));
Ri_p8 <= not (not CLK and not aux and (Ro_p7));
Ri_p7 <= not (CLK and (Ro_p5));
Ri_p4 <= not (not CLK and (Ro_p2));
Ri_p15 <= not (not CLK and (Ro_p14));
Ri_p19 <= not (not CLK and not aux and (Ro_p18));
Ri_p10 <= not (not SDA and CLK and (Ro_p1));
Ri_p1 <= not (reset or (Ro_p15) or (Ro_p19) or (Ro_p8) or (not CLK and (Ro_p9));
Ri_p3 <= not (aux and (Ro_p2));
Ri_p12 <= not (not CLK and (Ro_p10));
Ri_p5 <= not (not CLK and (Ro_p3));
Ri_p16 <= not (not CLK and (Ro_p11));
Ri_p11 <= not (aux and (Ro_p10));
Ri_p9 <= not (CLK and (Ro_p4));
Ri_p18 <= not (CLK and (Ro_p16));
Ri_p14 <= not (CLK and (Ro_p12));


Ai_p2 <= not reset and (Ao_p3 and Ao_p4);
Ai_p8 <= not reset and (Ao_p1);
Ai_p7 <= not reset and (Ao_p8);
Ai_p4 <= not reset and (Ao_p9);
Ai_p15 <= not reset and (Ao_p1);
Ai_p19 <= not reset and (Ao_p1);
Ai_p10 <= not reset and (Ao_p11 and Ao_p12);
Ai_p1 <= (Ao_p2 and Ao_p10);
Ai_p3 <= not reset and (Ao_p5);
Ai_p12 <= not reset and (Ao_p14);
Ai_p5 <= not reset and (Ao_p7);
Ai_p16 <= not reset and (Ao_p18);
Ai_p11 <= not reset and (Ao_p16);
Ai_p9 <= not reset and (Ao_p1);
Ai_p18 <= not reset and (Ao_p19);
Ai_p14 <= not reset and (Ao_p15);


a_set <= not((Ro_p5) or (Ro_p12)) or not a_reset;
a_reset <= not reset and (not((Ro_p8) or (Ro_p15)));

b_set <= not((Ro_p12) or (Ro_p16)) or not b_reset;
b_reset <= not reset and (not((Ro_p19) or (Ro_p15)));

end struct;
