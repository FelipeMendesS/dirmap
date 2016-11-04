---------------------------------------------
-- testFile5
-- by Felipe Mendes dos Santos, 03/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity testFile5 is
port(reset :in  std_logic;
     c: in  std_logic;
     a: in  std_logic;
     b: in  std_logic;
     y: out std_logic;
     x: out std_logic);
end testFile5;

---------------------------------------------

architecture struct of testFile5 is

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

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

signal Ri_p9: std_logic;
signal Ai_p9: std_logic;
signal Ro_p9: std_logic;
signal Ao_p9: std_logic;

signal Ri_p11: std_logic;
signal Ai_p11: std_logic;
signal Ro_p11: std_logic;
signal Ao_p11: std_logic;

signal Ri_p5: std_logic;
signal Ai_p5: std_logic;
signal Ro_p5: std_logic;
signal Ao_p5: std_logic;

signal Ri_p3: std_logic;
signal Ai_p3: std_logic;
signal Ro_p3: std_logic;
signal Ao_p3: std_logic;

signal y_set:   std_logic;
signal y_reset: std_logic;

signal x_set:   std_logic;
signal x_reset: std_logic;

begin

p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p9: control_cell port map (Ri_p9, Ai_p9, Ro_p9, Ao_p9);
p11: control_cell port map (Ri_p11, Ai_p11, Ro_p11, Ao_p11);
p5: control_cell port map (Ri_p5, Ai_p5, Ro_p5, Ao_p5);
p3: control_cell port map (Ri_p3, Ai_p3, Ro_p3, Ao_p3);

y_cell: output_cell port map (y_set, y_reset, y);
x_cell: output_cell port map (x_set, x_reset, x);

Ri_p1 <= not (reset or (Ro_p11 and Ro_p5));
Ri_p6 <= not (b and (Ro_p1));
Ri_p9 <= not (c and (Ro_p1));
Ri_p11 <= not (not c and (Ro_p9));
Ri_p5 <= not ((not a and (Ro_p3) or (not b and (Ro_p6) or );
Ri_p3 <= not (a and (Ro_p1));


Ai_p1 <= ((Ao_p3 and Ao_p6) or Ao_p9);
Ai_p6 <= not reset and (Ao_p5);
Ai_p9 <= not reset and (Ao_p11);
Ai_p11 <= not reset and (Ao_p1);
Ai_p5 <= not reset and (Ao_p1);
Ai_p3 <= not reset and (Ao_p5);


