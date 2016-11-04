---------------------------------------------
-- atod
-- by Felipe Mendes dos Santos, 03/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity atod is
port(la: in  std_logic;
     da: in  std_logic;
     za: in  std_logic;
     x:  out std_logic;
     dr: out std_logic;
     lr: out std_logic;
     zr: out std_logic;
);
end atod;

---------------------------------------------

architecture struct of atod is

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

signal Ri_PL5: std_logic;
signal Ai_PL5: std_logic;
signal Ro_PL5: std_logic;
signal Ao_PL5: std_logic;

signal Ri_PL3: std_logic;
signal Ai_PL3: std_logic;
signal Ro_PL3: std_logic;
signal Ao_PL3: std_logic;

signal Ri_PL8: std_logic;
signal Ai_PL8: std_logic;
signal Ro_PL8: std_logic;
signal Ao_PL8: std_logic;

signal Ri_PL1: std_logic;
signal Ai_PL1: std_logic;
signal Ro_PL1: std_logic;
signal Ao_PL1: std_logic;

signal Ri_PL17: std_logic;
signal Ai_PL17: std_logic;
signal Ro_PL17: std_logic;
signal Ao_PL17: std_logic;

signal Ri_PL12: std_logic;
signal Ai_PL12: std_logic;
signal Ro_PL12: std_logic;
signal Ao_PL12: std_logic;

signal x_set:   std_logic
signal x_reset: std_logic

signal dr_set:   std_logic
signal dr_reset: std_logic

signal lr_set:   std_logic
signal lr_reset: std_logic

signal zr_set:   std_logic
signal zr_reset: std_logic

begin

PL5: control_cell port map (Ri_PL5, Ai_PL5, Ro_PL5, Ao_PL5);
PL3: control_cell port map (Ri_PL3, Ai_PL3, Ro_PL3, Ao_PL3);
PL8: control_cell port map (Ri_PL8, Ai_PL8, Ro_PL8, Ao_PL8);
PL1: control_cell port map (Ri_PL1, Ai_PL1, Ro_PL1, Ao_PL1);
PL17: control_cell port map (Ri_PL17, Ai_PL17, Ro_PL17, Ao_PL17);
PL12: control_cell port map (Ri_PL12, Ai_PL12, Ro_PL12, Ao_PL12);

x_cell: output_cell port map (x_set, x_reset, x);
dr_cell: output_cell port map (dr_set, dr_reset, dr);
lr_cell: output_cell port map (lr_set, lr_reset, lr);
zr_cell: output_cell port map (zr_set, zr_reset, zr);

Ri_PL5 <= not (za and (Ro_PL1 and Ro_PL3))
Ri_PL3 <= not (da and (Ro_PL1))
Ri_PL8 <= not (not za and (Ro_PL5))
Ri_PL1 <= not (reset or (la and (Ro_PL12 and Ro_PL8))
Ri_PL17 <= not (not la and (Ro_PL1))
Ri_PL12 <= not (not da and (Ro_PL5 and Ro_PL17))
