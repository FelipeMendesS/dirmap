---------------------------------------------
-- ALU2-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity ALU2_vf is
port(reset :in  std_logic;
     M2A2:   in  std_logic;
     M1A:    in  std_logic;
     C:      in  std_logic;
     EvDone: in  std_logic;
     start:  in  std_logic;
     selym2: out std_logic;
     seldx:  out std_logic;
     Prech:  out std_logic;
     LY:     out std_logic;
     LX:     out std_logic;
     EndP:   out std_logic;
     A2M:    out std_logic);
end ALU2_vf;

---------------------------------------------

architecture struct of ALU2_vf is

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

signal Ri_p12: std_logic;
signal Ai_p12: std_logic;
signal Ro_p12: std_logic;
signal Ao_p12: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p26: std_logic;
signal Ai_p26: std_logic;
signal Ro_p26: std_logic;
signal Ao_p26: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p20: std_logic;
signal Ai_p20: std_logic;
signal Ro_p20: std_logic;
signal Ao_p20: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p24: std_logic;
signal Ai_p24: std_logic;
signal Ro_p24: std_logic;
signal Ao_p24: std_logic;

signal Ri_p30: std_logic;
signal Ai_p30: std_logic;
signal Ro_p30: std_logic;
signal Ao_p30: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p29: std_logic;
signal Ai_p29: std_logic;
signal Ro_p29: std_logic;
signal Ao_p29: std_logic;

signal Ri_p22: std_logic;
signal Ai_p22: std_logic;
signal Ro_p22: std_logic;
signal Ao_p22: std_logic;

signal Ri_p28: std_logic;
signal Ai_p28: std_logic;
signal Ro_p28: std_logic;
signal Ao_p28: std_logic;

signal selym2_set:   std_logic;
signal selym2_reset: std_logic;

signal seldx_set:   std_logic;
signal seldx_reset: std_logic;

signal Prech_set:   std_logic;
signal Prech_reset: std_logic;

signal LY_set:   std_logic;
signal LY_reset: std_logic;

signal LX_set:   std_logic;
signal LX_reset: std_logic;

signal EndP_set:   std_logic;
signal EndP_reset: std_logic;

signal A2M_set:   std_logic;
signal A2M_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p26: control_cell port map (Ri_p26, Ai_p26, Ro_p26, Ao_p26);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p20: control_cell port map (Ri_p20, Ai_p20, Ro_p20, Ao_p20);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p24: control_cell port map (Ri_p24, Ai_p24, Ro_p24, Ao_p24);
p30: control_cell port map (Ri_p30, Ai_p30, Ro_p30, Ao_p30);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p29: control_cell port map (Ri_p29, Ai_p29, Ro_p29, Ao_p29);
p22: control_cell port map (Ri_p22, Ai_p22, Ro_p22, Ao_p22);
p28: control_cell port map (Ri_p28, Ai_p28, Ro_p28, Ao_p28);

selym2_cell: output_cell port map (selym2_set, selym2_reset, selym2);
seldx_cell: output_cell port map (seldx_set, seldx_reset, seldx);
Prech_cell: output_cell port map (Prech_set, Prech_reset, Prech);
LY_cell: output_cell port map (LY_set, LY_reset, LY);
LX_cell: output_cell port map (LX_set, LX_reset, LX);
EndP_cell: output_cell port map (EndP_set, EndP_reset, EndP);
A2M_cell: output_cell port map (A2M_set, A2M_reset, A2M);

Ri_p2 <= not (start and (Ro_p1));
Ri_p6 <= not (not EvDone and (Ro_p4));
Ri_p16 <= not (EvDone and not M1A and not M2A2 and (Ro_p14));
Ri_p12 <= not (not C and EvDone and (Ro_p10));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p28)));
Ri_p26 <= not (not EvDone and (Ro_p29));
Ri_p4 <= not (not C and EvDone and (Ro_p2));
Ri_p20 <= not (not EvDone and (Ro_p30));
Ri_p18 <= not (not EvDone and (Ro_p16));
Ri_p24 <= not (not EvDone and (Ro_p22));
Ri_p30 <= not (C and EvDone and (Ro_p10));
Ri_p14 <= not (not EvDone and (Ro_p12));
Ri_p10 <= not (not EvDone and M1A and M2A2 and (Ro_p8));
Ri_p8 <= not (EvDone and (Ro_p18 or Ro_p6));
Ri_p29 <= not (C and EvDone and (Ro_p2));
Ri_p22 <= not (EvDone and not M1A and not M2A2 and (Ro_p20));
Ri_p28 <= not (not start and (Ro_p24 or Ro_p26));


Ai_p2 <= not reset and (Ao_p4 and Ao_p29);
Ai_p6 <= not reset and (Ao_p8);
Ai_p16 <= not reset and (Ao_p18);
Ai_p12 <= not reset and (Ao_p14);
Ai_p1 <= (Ao_p2);
Ai_p26 <= not reset and (Ao_p28);
Ai_p4 <= not reset and (Ao_p6);
Ai_p20 <= not reset and (Ao_p22);
Ai_p18 <= not reset and (Ao_p8);
Ai_p24 <= not reset and (Ao_p28);
Ai_p30 <= not reset and (Ao_p20);
Ai_p14 <= not reset and (Ao_p16);
Ai_p10 <= not reset and (Ao_p12 and Ao_p30);
Ai_p8 <= not reset and (Ao_p10);
Ai_p29 <= not reset and (Ao_p26);
Ai_p22 <= not reset and (Ao_p24);
Ai_p28 <= not reset and (Ao_p1);


selym2_set <= not((Ro_p30) or (Ro_p12)) or not selym2_reset;
selym2_reset <= not reset and (not((Ro_p16) or (Ro_p22)));

seldx_set <= not((Ro_p12) or (Ro_p4)) or not seldx_reset;
seldx_reset <= not reset and (not((Ro_p8)));

Prech_set <= not reset and (not((Ro_p16) or (Ro_p30) or (Ro_p8) or (Ro_p12) or (Ro_p4) or (Ro_p29) or (Ro_p22)) or not Prech_reset;
Prech_reset <= not((Ro_p10) or (Ro_p14) or (Ro_p2) or (Ro_p18) or (Ro_p20) or (Ro_p6)));

LY_set <= not((Ro_p16) or (Ro_p22)) or not LY_reset;
LY_reset <= not reset and (not((Ro_p24) or (Ro_p18)));

LX_set <= not((Ro_p8)) or not LX_reset;
LX_reset <= not reset and (not((Ro_p14) or (Ro_p20)));

EndP_set <= not((Ro_p24) or (Ro_p26)) or not EndP_reset;
EndP_reset <= not reset and (not((Ro_p28)));

A2M_set <= not((Ro_p16) or (Ro_p4)) or not A2M_reset;
A2M_reset <= not reset and (not((Ro_p10)));

end struct;
