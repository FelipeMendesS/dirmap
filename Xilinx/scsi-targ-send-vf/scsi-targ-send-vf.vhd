---------------------------------------------
-- scsi-targ-send-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity scsi_targ_send_vf is
port(reset :in  std_logic;
     empty:        in  std_logic;
     ackin:        in  std_logic;
     startdmasend: in  std_logic;
     dack:         in  std_logic;
     done:         in  std_logic;
     dtc:          in  std_logic;
     reqout:       out std_logic;
     ready:        out std_logic;
     dreq:         out std_logic;
     enddmaint:    out std_logic);
end scsi_targ_send_vf;

---------------------------------------------

architecture struct of scsi_targ_send_vf is

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

signal Ri_p20: std_logic;
signal Ai_p20: std_logic;
signal Ro_p20: std_logic;
signal Ao_p20: std_logic;

signal Ri_p26: std_logic;
signal Ai_p26: std_logic;
signal Ro_p26: std_logic;
signal Ao_p26: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p14: std_logic;
signal Ai_p14: std_logic;
signal Ro_p14: std_logic;
signal Ao_p14: std_logic;

signal Ri_p24: std_logic;
signal Ai_p24: std_logic;
signal Ro_p24: std_logic;
signal Ao_p24: std_logic;

signal Ri_p30: std_logic;
signal Ai_p30: std_logic;
signal Ro_p30: std_logic;
signal Ao_p30: std_logic;

signal Ri_p10: std_logic;
signal Ai_p10: std_logic;
signal Ro_p10: std_logic;
signal Ao_p10: std_logic;

signal Ri_p31: std_logic;
signal Ai_p31: std_logic;
signal Ro_p31: std_logic;
signal Ao_p31: std_logic;

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

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal Ri_Paux2: std_logic;
signal Ai_Paux2: std_logic;
signal Ro_Paux2: std_logic;
signal Ao_Paux2: std_logic;

signal reqout_set:   std_logic;
signal reqout_reset: std_logic;

signal ready_set:   std_logic;
signal ready_reset: std_logic;

signal dreq_set:   std_logic;
signal dreq_reset: std_logic;

signal enddmaint_set:   std_logic;
signal enddmaint_reset: std_logic;

begin

p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p20: control_cell port map (Ri_p20, Ai_p20, Ro_p20, Ao_p20);
p26: control_cell port map (Ri_p26, Ai_p26, Ro_p26, Ao_p26);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p24: control_cell port map (Ri_p24, Ai_p24, Ro_p24, Ao_p24);
p30: control_cell port map (Ri_p30, Ai_p30, Ro_p30, Ao_p30);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p31: control_cell port map (Ri_p31, Ai_p31, Ro_p31, Ao_p31);
p29: control_cell port map (Ri_p29, Ai_p29, Ro_p29, Ao_p29);
p22: control_cell port map (Ri_p22, Ai_p22, Ro_p22, Ao_p22);
p28: control_cell port map (Ri_p28, Ai_p28, Ro_p28, Ao_p28);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);

Paux2: control_cell port map (Ri_Paux2, Ai_Paux2, Ro_Paux2, Ao_Paux2);

reqout_cell: output_cell port map (reqout_set, reqout_reset, reqout);
ready_cell: output_cell port map (ready_set, ready_reset, ready);
dreq_cell: output_cell port map (dreq_set, dreq_reset, dreq);
enddmaint_cell: output_cell port map (enddmaint_set, enddmaint_reset, enddmaint);

Ri_p2 <= not (startdmasend and (Ro_p1));
Ri_p16 <= not (not dack and not dtc and (Ro_p31));
Ri_p12 <= not (dack and (Ro_p10));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p30)));
Ri_p20 <= not (empty and dack and not ackin and (Ro_p18 or Ro_p22));
Ri_p26 <= not (ackin and (Ro_Paux2 or Ro_p24));
Ri_p18 <= not (ackin and (Ro_p16));
Ri_p14 <= not (done and dtc and (Ro_p20 or Ro_p12));
Ri_p24 <= not (not dack and not dtc and (Ro_p14));
Ri_p30 <= not (empty and not ackin and (Ro_p26));
Ri_p10 <= not (not startdmasend and (Ro_p2));
Ri_p31 <= not (not done and dtc and (Ro_p20 or Ro_p12));
Ri_p29 <= not (not empty and not ackin and (Ro_p18 or Ro_p22));
Ri_p22 <= not (ackin and (Ro_Paux1));
Ri_p28 <= not (not empty and not ackin and (Ro_p26));

Ri_Paux1 <= not (Ro_p29 and Ai_Paux1);
Ri_Paux2 <= not (Ro_p28 and Ai_Paux2);

Ai_p2 <= not reset and (Ao_p10);
Ai_p16 <= not reset and (Ao_p18);
Ai_p12 <= not reset and (Ao_p31 and Ao_p14);
Ai_p1 <= (Ao_p2);
Ai_p20 <= not reset and (Ao_p31 and Ao_p14);
Ai_p26 <= not reset and (Ao_p28 and Ao_p30);
Ai_p18 <= not reset and (Ao_p20 and Ao_p29);
Ai_p14 <= not reset and (Ao_p24);
Ai_p24 <= not reset and (Ao_p26);
Ai_p30 <= not reset and (Ao_p1);
Ai_p10 <= not reset and (Ao_p12);
Ai_p31 <= not reset and (Ao_p16);
Ai_p29 <= not reset and (Ao_Paux1);
Ai_p22 <= not reset and (Ao_p20 and Ao_p29);
Ai_p28 <= not reset and (Ao_Paux2);

Ai_Paux1 <= not reset and (Ao_p22);
Ai_Paux2 <= not reset and (Ao_p26);

reqout_set <= not((Ro_p24) or (Ro_Paux2) or (Ro_p16) or (Ro_Paux1)) or not reqout_reset;
reqout_reset <= not reset and (not((Ro_p26) or (Ro_p18) or (Ro_p22)));

ready_set <= not((Ro_p20) or (Ro_p12)) or not ready_reset;
ready_reset <= not reset and (not((Ro_p14) or (Ro_p31)));

dreq_set <= not((Ro_p10)) or not dreq_reset;
dreq_reset <= not reset and (not((Ro_p14)));

enddmaint_set <= not reset and (not((Ro_p30)) or not enddmaint_reset;
enddmaint_reset <= not((Ro_p2)));

end struct;
