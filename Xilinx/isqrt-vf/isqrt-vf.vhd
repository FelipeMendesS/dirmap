---------------------------------------------
-- isqrt-vf
-- by Felipe Mendes dos Santos, 05/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity isqrt_vf is
port(reset :in  std_logic;
     m:     in  std_logic;
     bt:    in  std_logic;
     eq:    in  std_logic;
     Req:   in  std_logic;
     me:    in  std_logic;
     ct:    out std_logic;
     sa:    out std_logic;
     lr:    out std_logic;
     ln:    out std_logic;
     sn:    out std_logic;
     sf:    out std_logic;
     lc:    out std_logic;
     lb:    out std_logic;
     clear: out std_logic;
     Ack:   out std_logic);
end isqrt_vf;

---------------------------------------------

architecture struct of isqrt_vf is

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

signal Ri_p40: std_logic;
signal Ai_p40: std_logic;
signal Ro_p40: std_logic;
signal Ao_p40: std_logic;

signal Ri_p34: std_logic;
signal Ai_p34: std_logic;
signal Ro_p34: std_logic;
signal Ao_p34: std_logic;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p20: std_logic;
signal Ai_p20: std_logic;
signal Ro_p20: std_logic;
signal Ao_p20: std_logic;

signal Ri_p43: std_logic;
signal Ai_p43: std_logic;
signal Ro_p43: std_logic;
signal Ao_p43: std_logic;

signal Ri_p36: std_logic;
signal Ai_p36: std_logic;
signal Ro_p36: std_logic;
signal Ao_p36: std_logic;

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

signal Ri_p38: std_logic;
signal Ai_p38: std_logic;
signal Ro_p38: std_logic;
signal Ao_p38: std_logic;

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

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

signal Ri_p42: std_logic;
signal Ai_p42: std_logic;
signal Ro_p42: std_logic;
signal Ao_p42: std_logic;

signal Ri_p24: std_logic;
signal Ai_p24: std_logic;
signal Ro_p24: std_logic;
signal Ao_p24: std_logic;

signal Ri_p28: std_logic;
signal Ai_p28: std_logic;
signal Ro_p28: std_logic;
signal Ao_p28: std_logic;

signal Ri_p41: std_logic;
signal Ai_p41: std_logic;
signal Ro_p41: std_logic;
signal Ao_p41: std_logic;

signal Ri_p16: std_logic;
signal Ai_p16: std_logic;
signal Ro_p16: std_logic;
signal Ao_p16: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p18: std_logic;
signal Ai_p18: std_logic;
signal Ro_p18: std_logic;
signal Ao_p18: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p22: std_logic;
signal Ai_p22: std_logic;
signal Ro_p22: std_logic;
signal Ao_p22: std_logic;

signal Ri_p32: std_logic;
signal Ai_p32: std_logic;
signal Ro_p32: std_logic;
signal Ao_p32: std_logic;

signal ct_set:   std_logic;
signal ct_reset: std_logic;

signal sa_set:   std_logic;
signal sa_reset: std_logic;

signal lr_set:   std_logic;
signal lr_reset: std_logic;

signal ln_set:   std_logic;
signal ln_reset: std_logic;

signal sn_set:   std_logic;
signal sn_reset: std_logic;

signal sf_set:   std_logic;
signal sf_reset: std_logic;

signal lc_set:   std_logic;
signal lc_reset: std_logic;

signal lb_set:   std_logic;
signal lb_reset: std_logic;

signal clear_set:   std_logic;
signal clear_reset: std_logic;

signal Ack_set:   std_logic;
signal Ack_reset: std_logic;

begin

p40: control_cell port map (Ri_p40, Ai_p40, Ro_p40, Ao_p40);
p34: control_cell port map (Ri_p34, Ai_p34, Ro_p34, Ao_p34);
p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p20: control_cell port map (Ri_p20, Ai_p20, Ro_p20, Ao_p20);
p43: control_cell port map (Ri_p43, Ai_p43, Ro_p43, Ao_p43);
p36: control_cell port map (Ri_p36, Ai_p36, Ro_p36, Ao_p36);
p30: control_cell port map (Ri_p30, Ai_p30, Ro_p30, Ao_p30);
p14: control_cell port map (Ri_p14, Ai_p14, Ro_p14, Ao_p14);
p10: control_cell port map (Ri_p10, Ai_p10, Ro_p10, Ao_p10);
p38: control_cell port map (Ri_p38, Ai_p38, Ro_p38, Ao_p38);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p12: control_cell port map (Ri_p12, Ai_p12, Ro_p12, Ao_p12);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p26: control_cell port map (Ri_p26, Ai_p26, Ro_p26, Ao_p26);
p42: control_cell port map (Ri_p42, Ai_p42, Ro_p42, Ao_p42);
p24: control_cell port map (Ri_p24, Ai_p24, Ro_p24, Ao_p24);
p28: control_cell port map (Ri_p28, Ai_p28, Ro_p28, Ao_p28);
p41: control_cell port map (Ri_p41, Ai_p41, Ro_p41, Ao_p41);
p16: control_cell port map (Ri_p16, Ai_p16, Ro_p16, Ao_p16);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p18: control_cell port map (Ri_p18, Ai_p18, Ro_p18, Ao_p18);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p22: control_cell port map (Ri_p22, Ai_p22, Ro_p22, Ao_p22);
p32: control_cell port map (Ri_p32, Ai_p32, Ro_p32, Ao_p32);

ct_cell: output_cell port map (ct_set, ct_reset, ct);
sa_cell: output_cell port map (sa_set, sa_reset, sa);
lr_cell: output_cell port map (lr_set, lr_reset, lr);
ln_cell: output_cell port map (ln_set, ln_reset, ln);
sn_cell: output_cell port map (sn_set, sn_reset, sn);
sf_cell: output_cell port map (sf_set, sf_reset, sf);
lc_cell: output_cell port map (lc_set, lc_reset, lc);
lb_cell: output_cell port map (lb_set, lb_reset, lb);
clear_cell: output_cell port map (clear_set, clear_reset, clear);
Ack_cell: output_cell port map (Ack_set, Ack_reset, Ack);

Ri_p40 <= not (not bt and (Ro_p36));
Ri_p34 <= not (not bt and (Ro_p30 or Ro_p32));
Ri_p2 <= not (Req and (Ro_p1));
Ri_p20 <= not (not bt and (Ro_p18));
Ri_p43 <= not (not me and not bt and (Ro_p14));
Ri_p36 <= not (bt and (Ro_p34));
Ri_p30 <= not (bt and (Ro_p28));
Ri_p14 <= not (not eq and bt and (Ro_p40 or Ro_p42));
Ri_p10 <= not (not bt and (Ro_p8));
Ri_p38 <= not (not Req and not bt and (Ro_p41));
Ri_p6 <= not (m and not bt and (Ro_p12 or Ro_p4));
Ri_p12 <= not (bt and (Ro_p10));
Ri_p1 <= not (reset or (Ai_p1 and (Ro_p38)));
Ri_p26 <= not (bt and (Ro_p24));
Ri_p42 <= not (not m and not bt and (Ro_p12 or Ro_p4));
Ri_p24 <= not (not bt and (Ro_p22));
Ri_p28 <= not (not bt and (Ro_p26));
Ri_p41 <= not (eq and bt and (Ro_p40 or Ro_p42));
Ri_p16 <= not (me and not bt and (Ro_p14));
Ri_p4 <= not (bt and (Ro_p2));
Ri_p18 <= not (bt and (Ro_p16));
Ri_p8 <= not (bt and (Ro_p6));
Ri_p22 <= not (bt and (Ro_p20));
Ri_p32 <= not (bt and (Ro_p43));


Ai_p40 <= not reset and (Ao_p14 and Ao_p41);
Ai_p34 <= not reset and (Ao_p36);
Ai_p2 <= not reset and (Ao_p4);
Ai_p20 <= not reset and (Ao_p22);
Ai_p43 <= not reset and (Ao_p32);
Ai_p36 <= not reset and (Ao_p40);
Ai_p30 <= not reset and (Ao_p34);
Ai_p14 <= not reset and (Ao_p16 and Ao_p43);
Ai_p10 <= not reset and (Ao_p12);
Ai_p38 <= not reset and (Ao_p1);
Ai_p6 <= not reset and (Ao_p8);
Ai_p12 <= not reset and (Ao_p6 and Ao_p42);
Ai_p1 <= (Ao_p2);
Ai_p26 <= not reset and (Ao_p28);
Ai_p42 <= not reset and (Ao_p14 and Ao_p41);
Ai_p24 <= not reset and (Ao_p26);
Ai_p28 <= not reset and (Ao_p30);
Ai_p41 <= not reset and (Ao_p38);
Ai_p16 <= not reset and (Ao_p18);
Ai_p4 <= not reset and (Ao_p6 and Ao_p42);
Ai_p18 <= not reset and (Ao_p20);
Ai_p8 <= not reset and (Ao_p10);
Ai_p22 <= not reset and (Ao_p24);
Ai_p32 <= not reset and (Ao_p34);


ct_set <= not((Ro_p10) or (Ro_p16) or (Ro_p2) or (Ro_p42) or (Ro_p34) or (Ro_p28) or (Ro_p20) or (Ro_p24) or (Ro_p43) or (Ro_p40) or (Ro_p6)) or not ct_reset;
ct_reset <= not reset and (not((Ro_p14) or (Ro_p30) or (Ro_p12) or (Ro_p26) or (Ro_p36) or (Ro_p8) or (Ro_p4) or (Ro_p22) or (Ro_p32) or (Ro_p18) or (Ro_p41)));

sa_set <= not((Ro_p32) or (Ro_p24) or (Ro_p6)) or not sa_reset;
sa_reset <= not reset and (not((Ro_p12) or (Ro_p36)));

lr_set <= not((Ro_p26) or (Ro_p22) or (Ro_p43)) or not lr_reset;
lr_reset <= not reset and (not((Ro_p28) or (Ro_p32) or (Ro_p24)));

ln_set <= not((Ro_p2) or (Ro_p18)) or not ln_reset;
ln_reset <= not reset and (not((Ro_p4) or (Ro_p22)));

sn_set <= not((Ro_p20)) or not sn_reset;
sn_reset <= not reset and (not((Ro_p26)));

sf_set <= not((Ro_p16)) or not sf_reset;
sf_reset <= not reset and (not((Ro_p26)));

lc_set <= not((Ro_p14) or (Ro_p22)) or not lc_reset;
lc_reset <= not reset and (not((Ro_p16) or (Ro_p24) or (Ro_p43)));

lb_set <= not((Ro_p2) or (Ro_p8) or (Ro_p34)) or not lb_reset;
lb_reset <= not reset and (not((Ro_p10) or (Ro_p36) or (Ro_p4)));

clear_set <= not reset and (not((Ro_p38)) or not clear_reset;
clear_reset <= not((Ro_p2)));

Ack_set <= not((Ro_p41)) or not Ack_reset;
Ack_reset <= not reset and (not((Ro_p38)));

end struct;
