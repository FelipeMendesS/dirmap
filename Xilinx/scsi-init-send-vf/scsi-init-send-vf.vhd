---------------------------------------------
-- scsi-init-send-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity scsi_init_send_vf is
port(reset :in  std_logic;
     rin:    in  std_logic;
     cntgt1: in  std_logic;
     fain:   in  std_logic;
     dsel:   in  std_logic;
     ok:     in  std_logic;
     aout:   out std_logic;
     sel:    out std_logic;
     frout:  out std_logic);
end scsi_init_send_vf;

---------------------------------------------

architecture struct of scsi_init_send_vf is

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

signal Ri_p20: std_logic;
signal Ai_p20: std_logic;
signal Ro_p20: std_logic;
signal Ao_p20: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p19: std_logic;
signal Ai_p19: std_logic;
signal Ro_p19: std_logic;
signal Ao_p19: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal aout_set:   std_logic;
signal aout_reset: std_logic;

signal sel_set:   std_logic;
signal sel_reset: std_logic;

signal frout_set:   std_logic;
signal frout_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p20: control_cell port map (Ri_p20, Ai_p20, Ro_p20, Ao_p20);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p19: control_cell port map (Ri_p19, Ai_p19, Ro_p19, Ao_p19);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);

aout_cell: output_cell port map (aout_set, aout_reset, aout);
sel_cell: output_cell port map (sel_set, sel_reset, sel);
frout_cell: output_cell port map (frout_set, frout_reset, frout);

Ri_p2 <= not (ok and (Ro_p1));
Ri_p6 <= not (rin and not fain and (Ro_p4));
Ri_p12 <= not (cntgt1 and not rin and (Ro_p10));
Ri_p16 <= not (rin and not fain and (Ro_p14));
Ri_p20 <= not (not cntgt1 and not rin and (Ro_p16 or Ro_p6));
Ri_p1 <= not (reset or (not ok and (Ro_p19 or Ro_p20));
Ri_p4 <= not (fain and (Ro_p2));
Ri_p19 <= not (not cntgt1 and not rin and (Ro_p10));
Ri_p8 <= not (cntgt1 and not rin and not dsel and (Ro_p16 or Ro_p6));
Ri_p14 <= not (fain and (Ro_p12));
Ri_p10 <= not (rin and dsel and (Ro_p8));


Ai_p2 <= not reset and (Ao_p4);
Ai_p6 <= not reset and (Ao_p8 and Ao_p20);
Ai_p12 <= not reset and (Ao_p14);
Ai_p16 <= not reset and (Ao_p8 and Ao_p20);
Ai_p20 <= not reset and (Ao_p1);
Ai_p1 <= (Ao_p2);
Ai_p4 <= not reset and (Ao_p6);
Ai_p19 <= not reset and (Ao_p1);
Ai_p8 <= not reset and (Ao_p10);
Ai_p14 <= not reset and (Ao_p16);
Ai_p10 <= not reset and (Ao_p12 and Ao_p19);


aout_set <= not((Ro_p6) or (Ro_p16) or (Ro_p10)) or not aout_reset;
aout_reset <= not reset and (not((Ro_p19) or (Ro_p12) or (Ro_p20) or (Ro_p8)));

sel_set <= not((Ro_p8)) or not sel_reset;
sel_reset <= not reset and (not((Ro_p19) or (Ro_p12)));

frout_set <= not((Ro_p2) or (Ro_p12)) or not frout_reset;
frout_reset <= not reset and (not((Ro_p14) or (Ro_p4)));

end struct;
