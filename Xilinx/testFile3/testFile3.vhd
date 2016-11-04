---------------------------------------------
-- testFile3
-- by Felipe Mendes dos Santos, 03/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity testFile3 is
port(a: in  std_logic;
     d: in  std_logic;
     c: out std_logic;
     b: out std_logic;
     x: out std_logic;
);
end testFile3;

---------------------------------------------

architecture struct of testFile3 is

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

signal Ri_8: std_logic;
signal Ai_8: std_logic;
signal Ro_8: std_logic;
signal Ao_8: std_logic;

signal Ri_12: std_logic;
signal Ai_12: std_logic;
signal Ro_12: std_logic;
signal Ao_12: std_logic;

signal Ri_1: std_logic;
signal Ai_1: std_logic;
signal Ro_1: std_logic;
signal Ao_1: std_logic;

signal Ri_5: std_logic;
signal Ai_5: std_logic;
signal Ro_5: std_logic;
signal Ao_5: std_logic;

signal c_set:   std_logic
signal c_reset: std_logic

signal b_set:   std_logic
signal b_reset: std_logic

signal x_set:   std_logic
signal x_reset: std_logic

begin

8: control_cell port map (Ri_8, Ai_8, Ro_8, Ao_8);
12: control_cell port map (Ri_12, Ai_12, Ro_12, Ao_12);
1: control_cell port map (Ri_1, Ai_1, Ro_1, Ao_1);
5: control_cell port map (Ri_5, Ai_5, Ro_5, Ao_5);

c_cell: output_cell port map (c_set, c_reset, c);
b_cell: output_cell port map (b_set, b_reset, b);
x_cell: output_cell port map (x_set, x_reset, x);

Ri_8 <= not (a and (Ro_5))
Ri_12 <= not ((not d and (Ro_8) or (not a and (