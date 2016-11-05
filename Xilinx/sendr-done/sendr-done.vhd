---------------------------------------------
-- sendr-done
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity sendr_done is
port(reset :in  std_logic;
     w8:           in  std_logic;
     reqsend:      in  std_logic;
     y0_sendrdone: out std_logic;
     dones:        out std_logic);
end sendr_done;

---------------------------------------------

architecture struct of sendr_done is

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

signal Ri_PL2: std_logic;
signal Ai_PL2: std_logic;
signal Ro_PL2: std_logic;
signal Ao_PL2: std_logic;

signal Ri_PL1: std_logic;
signal Ai_PL1: std_logic;
signal Ro_PL1: std_logic;
signal Ao_PL1: std_logic;

signal Ri_PL5: std_logic;
signal Ai_PL5: std_logic;
signal Ro_PL5: std_logic;
signal Ao_PL5: std_logic;

signal Ri_PL3: std_logic;
signal Ai_PL3: std_logic;
signal Ro_PL3: std_logic;
signal Ao_PL3: std_logic;

signal Ri_PL9: std_logic;
signal Ai_PL9: std_logic;
signal Ro_PL9: std_logic;
signal Ao_PL9: std_logic;

signal Ri_PL7: std_logic;
signal Ai_PL7: std_logic;
signal Ro_PL7: std_logic;
signal Ao_PL7: std_logic;

signal y0_sendrdone_set:   std_logic;
signal y0_sendrdone_reset: std_logic;

signal dones_set:   std_logic;
signal dones_reset: std_logic;

begin

PL2: control_cell port map (Ri_PL2, Ai_PL2, Ro_PL2, Ao_PL2);
PL1: control_cell port map (Ri_PL1, Ai_PL1, Ro_PL1, Ao_PL1);
PL5: control_cell port map (Ri_PL5, Ai_PL5, Ro_PL5, Ao_PL5);
PL3: control_cell port map (Ri_PL3, Ai_PL3, Ro_PL3, Ao_PL3);
PL9: control_cell port map (Ri_PL9, Ai_PL9, Ro_PL9, Ao_PL9);
PL7: control_cell port map (Ri_PL7, Ai_PL7, Ro_PL7, Ao_PL7);

y0_sendrdone_cell: output_cell port map (y0_sendrdone_set, y0_sendrdone_reset, y0_sendrdone);
dones_cell: output_cell port map (dones_set, dones_reset, dones);

Ri_PL2 <= not (reset or (Ai_PL2 and (Ro_PL7)));
Ri_PL1 <= not (reset or (Ai_PL1 and (Ro_PL7)));
Ri_PL5 <= not (not w8 and (Ro_PL3 and Ro_PL9));
Ri_PL3 <= not (w8 and (Ro_PL1));
Ri_PL9 <= not (reqsend and (Ro_PL2));
Ri_PL7 <= not (not reqsend and (Ro_PL5));


Ai_PL2 <= (Ao_PL9);
Ai_PL1 <= (Ao_PL3);
Ai_PL5 <= not reset and (Ao_PL7);
Ai_PL3 <= not reset and (Ao_PL5);
Ai_PL9 <= not reset and (Ao_PL5);
Ai_PL7 <= not reset and (Ao_PL1 or Ao_PL2);


