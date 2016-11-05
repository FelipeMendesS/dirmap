---------------------------------------------
-- testFile4
-- by Felipe Mendes dos Santos, 04/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity testFile4 is
port(reset :in  std_logic;
     b: in  std_logic;
     a: in  std_logic;
     c: in  std_logic;
     y: out std_logic;
     z: out std_logic;
     x: out std_logic);
end testFile4;

---------------------------------------------

architecture struct of testFile4 is

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

signal Ri_p7: std_logic;
signal Ai_p7: std_logic;
signal Ro_p7: std_logic;
signal Ao_p7: std_logic;

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p5: std_logic;
signal Ai_p5: std_logic;
signal Ro_p5: std_logic;
signal Ao_p5: std_logic;

signal y_set:   std_logic;
signal y_reset: std_logic;

signal z_set:   std_logic;
signal z_reset: std_logic;

signal x_set:   std_logic;
signal x_reset: std_logic;

begin

p7: control_cell port map (Ri_p7, Ai_p7, Ro_p7, Ao_p7);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p5: control_cell port map (Ri_p5, Ai_p5, Ro_p5, Ao_p5);

y_cell: output_cell port map (y_set, y_reset, y);
z_cell: output_cell port map (z_set, z_reset, z);
x_cell: output_cell port map (x_set, x_reset, x);

Ri_p7 <= not (a and (Ro_p5));
Ri_p12 <= not (not a and (Ro_p10 and Ro_p7));
Ri_p4 <= not (not b and (Ro_p2));
Ri_p10 <= not (a and not b and (Ro_p5));
Ri_p2 <= not (c and b and (Ro_p1));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p12 or Ro_p4)));
Ri_p5 <= not (not c and b and (Ro_p1));


Ai_p7 <= not reset and (Ao_p12);
Ai_p12 <= not reset and (Ao_p1);
Ai_p4 <= not reset and (Ao_p1);
Ai_p10 <= not reset and (Ao_p12);
Ai_p2 <= not reset and (Ao_p4);
Ai_p1 <= (Ao_p2 and Ao_p5);
Ai_p5 <= not reset and (Ao_p7 or Ao_p10);


y_set <= not((Ro_p2)) or not y_reset;
y_reset <= not reset and (not((Ro_p4)));

z_set <= not((Ro_p10)) or not z_reset;
z_reset <= not reset and (not((Ro_p12)));

x_set <= not((Ro_p5)) or not x_reset;
x_reset <= not reset and (not((Ro_p7)));

end struct;
