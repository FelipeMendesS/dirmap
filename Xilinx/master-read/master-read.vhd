---------------------------------------------
-- MASTER-READ
-- by Felipe Mendes dos Santos, 03/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity MASTER-READ is
port(pri:  in  std_logic;
     pack: in  std_logic;
     di:   in  std_logic;
     ari:  in  std_logic;
     bprn: in  std_logic;
     xack: in  std_logic;
     mrdc: out std_logic;
     pdo:  out std_logic;
     x:    out std_logic;
     do:   out std_logic;
     busy: out std_logic;
     aro:  out std_logic;
     pro:  out std_logic;
     breq: out std_logic;
);
end MASTER-READ;

---------------------------------------------

architecture struct of MASTER-READ is

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

signal Ri_PL4: std_logic;
signal Ai_PL4: std_logic;
signal Ro_PL4: std_logic;
signal Ao_PL4: std_logic;

signal Ri_PL11: std_logic;
signal Ai_PL11: std_logic;
signal Ro_PL11: std_logic;
signal Ao_PL11: std_logic;

signal Ri_PL1: std_logic;
signal Ai_PL1: std_logic;
signal Ro_PL1: std_logic;
signal Ao_PL1: std_logic;

signal Ri_PL33: std_logic;
signal Ai_PL33: std_logic;
signal Ro_PL33: std_logic;
signal Ao_PL33: std_logic;

signal Ri_PL3: std_logic;
signal Ai_PL3: std_logic;
signal Ro_PL3: std_logic;
signal Ao_PL3: std_logic;

signal Ri_PL27: std_logic;
signal Ai_PL27: std_logic;
signal Ro_PL27: std_logic;
signal Ao_PL27: std_logic;

signal Ri_PL37: std_logic;
signal Ai_PL37: std_logic;
signal Ro_PL37: std_logic;
signal Ao_PL37: std_logic;

signal Ri_PL35: std_logic;
signal Ai_PL35: std_logic;
signal Ro_PL35: std_logic;
signal Ao_PL35: std_logic;

signal Ri_PL13: std_logic;
signal Ai_PL13: std_logic;
signal Ro_PL13: std_logic;
signal Ao_PL13: std_logic;

signal Ri_PL7: std_logic;
signal Ai_PL7: std_logic;
signal Ro_PL7: std_logic;
signal Ao_PL7: std_logic;

signal Ri_PL16: std_logic;
signal Ai_PL16: std_logic;
signal Ro_PL16: std_logic;
signal Ao_PL16: std_logic;

signal Ri_PL5: std_logic;
signal Ai_PL5: std_logic;
signal Ro_PL5: std_logic;
signal Ao_PL5: std_logic;

signal Ri_PL24: std_logic;
signal Ai_PL24: std_logic;
signal Ro_PL24: std_logic;
signal Ao_PL24: std_logic;

signal Ri_PL10: std_logic;
signal Ai_PL10: std_logic;
signal Ro_PL10: std_logic;
signal Ao_PL10: std_logic;

signal Ri_PL2: std_logic;
signal Ai_PL2: std_logic;
signal Ro_PL2: std_logic;
signal Ao_PL2: std_logic;

signal Ri_PL15: std_logic;
signal Ai_PL15: std_logic;
signal Ro_PL15: std_logic;
signal Ao_PL15: std_logic;

signal Ri_PL39: std_logic;
signal Ai_PL39: std_logic;
signal Ro_PL39: std_logic;
signal Ao_PL39: std_logic;

signal Ri_PL21: std_logic;
signal Ai_PL21: std_logic;
signal Ro_PL21: std_logic;
signal Ao_PL21: std_logic;

signal Ri_PL29: std_logic;
signal Ai_PL29: std_logic;
signal Ro_PL29: std_logic;
signal Ao_PL29: std_logic;

signal Ri_PL26: std_logic;
signal Ai_PL26: std_logic;
signal Ro_PL26: std_logic;
signal Ao_PL26: std_logic;

signal Ri_Paux0: std_logic;
signal Ai_Paux0: std_logic;
signal Ro_Paux0: std_logic;
signal Ao_Paux0: std_logic;

signal Ro_PL29_buffer: std_logic;

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal Ro_PL3_buffer: std_logic;

signal mrdc_set:   std_logic
signal mrdc_reset: std_logic

signal pdo_set:   std_logic
signal pdo_reset: std_logic

signal x_set:   std_logic
signal x_reset: std_logic

signal do_set:   std_logic
signal do_reset: std_logic

signal busy_set:   std_logic
signal busy_reset: std_logic

signal aro_set:   std_logic
signal aro_reset: std_logic

signal pro_set:   std_logic
signal pro_reset: std_logic

signal breq_set:   std_logic
signal breq_reset: std_logic

begin

PL4: control_cell port map (Ri_PL4, Ai_PL4, Ro_PL4, Ao_PL4);
PL11: control_cell port map (Ri_PL11, Ai_PL11, Ro_PL11, Ao_PL11);
PL1: control_cell port map (Ri_PL1, Ai_PL1, Ro_PL1, Ao_PL1);
PL33: control_cell port map (Ri_PL33, Ai_PL33, Ro_PL33, Ao_PL33);
PL3: control_cell port map (Ri_PL3, Ai_PL3, Ro_PL3, Ao_PL3);
PL27: control_cell port map (Ri_PL27, Ai_PL27, Ro_PL27, Ao_PL27);
PL37: control_cell port map (Ri_PL37, Ai_PL37, Ro_PL37, Ao_PL37);
PL35: control_cell port map (Ri_PL35, Ai_PL35, Ro_PL35, Ao_PL35);
PL13: control_cell port map (Ri_PL13, Ai_PL13, Ro_PL13, Ao_PL13);
PL7: control_cell port map (Ri_PL7, Ai_PL7, Ro_PL7, Ao_PL7);
PL16: control_cell port map (Ri_PL16, Ai_PL16, Ro_PL16, Ao_PL16);
PL5: control_cell port map (Ri_PL5, Ai_PL5, Ro_PL5, Ao_PL5);
PL24: control_cell port map (Ri_PL24, Ai_PL24, Ro_PL24, Ao_PL24);
PL10: control_cell port map (Ri_PL10, Ai_PL10, Ro_PL10, Ao_PL10);
PL2: control_cell port map (Ri_PL2, Ai_PL2, Ro_PL2, Ao_PL2);
PL15: control_cell port map (Ri_PL15, Ai_PL15, Ro_PL15, Ao_PL15);
PL39: control_cell port map (Ri_PL39, Ai_PL39, Ro_PL39, Ao_PL39);
PL21: control_cell port map (Ri_PL21, Ai_PL21, Ro_PL21, Ao_PL21);
PL29: control_cell port map (Ri_PL29, Ai_PL29, Ro_PL29, Ao_PL29);
PL26: control_cell port map (Ri_PL26, Ai_PL26, Ro_PL26, Ao_PL26);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);
buffer_1: buffer_n generic map(N => 8) port map (Ro_PL29, Ro_PL29_buffer);

Paux2: control_cell port map (Ri_Paux2, Ai_Paux2, Ro_Paux2, Ao_Paux2);
buffer_2: buffer_n generic map(N => 8) port map (Ro_PL3, Ro_PL3_buffer);

mrdc_cell: output_cell port map (mrdc_set, mrdc_reset, mrdc);
pdo_cell: output_cell port map (pdo_set, pdo_reset, pdo);
x_cell: output_cell port map (x_set, x_reset, x);
do_cell: output_cell port map (do_set, do_reset, do);
busy_cell: output_cell port map (busy_set, busy_reset, busy);
aro_cell: output_cell port map (aro_set, aro_reset, aro);
pro_cell: output_cell port map (pro_set, pro_reset, pro);
breq_cell: output_cell port map (breq_set, breq_reset, breq);

Ri_PL4 <= not (reset or (Ro_PL10 and Ro_PL15))
Ri_PL11 <= not (not di and (Ro_PL16 and (Ro_PL35 and Ro_PL7)))
Ri_PL1 <= not (reset or (Ro_PL26))
Ri_PL33 <= not (bprn and (Ro_PL29 and Ro_PL3))
Ri_PL3 <= not (reset or (Ro_PL39))
Ri_PL27 <= not (not pri and (Ro_PL24 and (Ro_PL29 and Ro_PL3)))
Ri_PL37 <= not (ari and (Ro_PL1))
Ri_PL35 <= not (pack and (Ro_PL4))
Ri_PL13 <= not (not xack and (Ro_PL11 and Ro_PL21 and Ro_PL39))
Ri_PL7 <= not (di and (Ro_PL5))
Ri_PL16 <= not (di and (Ro_PL5))
Ri_PL5 <= not (reset or (Ro_PL13 and (Ro_PL10 and Ro_PL15)))
Ri_PL24 <= not (not ari and (Ro_PL2 and Ro_PL37))
Ri_PL10 <= not (not di and (Ro_PL16 and (Ro_PL35 and Ro_PL7)))
Ri_PL2 <= not (reset or ((Ro_PL16 and (Ro_PL29 and Ro_PL3)) and Ro_PL27 and Ro_PL33))
Ri_PL15 <= not (not pack and (Ro_PL35 and Ro_PL7))
Ri_PL39 <= not (not bprn and ((Ro_PL16 and (Ro_PL29 and Ro_PL3)) and Ro_PL27 and Ro_PL33))
Ri_PL21 <= not (xack and (Ro_PL16))
Ri_PL29 <= not (pri and (Ro_PL2 and Ro_PL37))
Ri_PL26 <= not (not pri and (Ro_PL24 and (Ro_PL29 and Ro_PL3)))

Ri_Paux1 <= not Ro_PL29_buffer;
Ri_Paux2 <= not Ro_PL3_buffer;

Ai_PL4 <= ((Ao_PL35) or not (Ao_PL10 and Ao_PL15));
Ai_PL11 <= not reset and ((Ao_PL13) or not (Ao_PL16 and (Ao_PL35 and Ao_PL7)));
Ai_PL1 <= ((Ao_PL37) or not (Ao_PL26));
Ai_PL33 <= not reset and ((Ao_PL2 or Ao_PL39) or not (Ao_PL29 and Ao_PL3));
Ai_PL3 <= ((Ao_Paux2) or not (Ao_PL39));
Ai_PL27 <= not reset and ((Ao_PL2 or Ao_PL39) or not (Ao_PL24 and (Ao_PL29 and Ao_PL3)));
Ai_PL37 <= not reset and ((Ao_PL24 or Ao_PL29) or not (Ao_PL1));
Ai_PL35 <= not reset and ((Ao_PL15 or (Ao_PL10 or Ao_PL11)) or not (Ao_PL4));
Ai_PL13 <= not reset and ((Ao_PL5) or not (Ao_PL11 and Ao_PL21 and Ao_PL39));
Ai_PL7 <= not reset and ((Ao_PL15 or (Ao_PL10 or Ao_PL11)) or not (Ao_PL5));
Ai_PL16 <= not reset and (((Ao_PL10 or Ao_PL11) or (Ao_PL2 or Ao_PL39) or Ao_PL21) or not (Ao_PL5));
Ai_PL5 <= ((Ao_PL16 or Ao_PL7) or not (Ao_PL13 and (Ao_PL10 and Ao_PL15)));
Ai_PL24 <= not reset and ((Ao_PL26 or Ao_PL27) or not (Ao_PL2 and Ao_PL37));
Ai_PL10 <= not reset and ((Ao_PL5 or Ao_PL4) or not (Ao_PL16 and (Ao_PL35 and Ao_PL7)));
Ai_PL2 <= ((Ao_PL24 or Ao_PL29) or not ((Ao_PL16 and (Ao_PL29 and Ao_PL3)) and Ao_PL27 and Ao_PL33));
Ai_PL15 <= not reset and ((Ao_PL5 or Ao_PL4) or not (Ao_PL35 and Ao_PL7));
Ai_PL39 <= not reset and ((Ao_PL3 or Ao_PL13) or not ((Ao_PL16 and (Ao_PL29 and Ao_PL3)) and Ao_PL27 and Ao_PL33));
Ai_PL21 <= not reset and ((Ao_PL13) or not (Ao_PL16));
Ai_PL29 <= not reset and ((Ao_Paux1) or not (Ao_PL2 and Ao_PL37));
Ai_PL26 <= not reset and ((Ao_PL1) or not (Ao_PL24 and (Ao_PL29 and Ao_PL3)));

Ai_Paux1 <= not reset and (((Ao_PL26 or Ao_PL27) or (Ao_PL2 or Ao_PL39) or Ao_PL33) or not Ao_PL29);
Ai_Paux2 <= not reset and (((Ao_PL26 or Ao_PL27) or (Ao_PL2 or Ao_PL39) or Ao_PL33) or not Ao_PL3);

