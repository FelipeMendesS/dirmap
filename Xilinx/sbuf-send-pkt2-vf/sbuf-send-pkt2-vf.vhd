---------------------------------------------
-- sbuf-send-pkt2-vf
-- by Felipe Mendes dos Santos, 04/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity sbuf_send_pkt2_vf is
port(reset :in  std_logic;
     req:       in  std_logic;
     done:      in  std_logic;
     ackline:   in  std_logic;
     ack:       out std_logic;
     sendiline: out std_logic);
end sbuf_send_pkt2_vf;

---------------------------------------------

architecture struct of sbuf_send_pkt2_vf is

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

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p8: std_logic;
signal Ai_p8: std_logic;
signal Ro_p8: std_logic;
signal Ao_p8: std_logic;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p9: std_logic;
signal Ai_p9: std_logic;
signal Ro_p9: std_logic;
signal Ao_p9: std_logic;

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal Ro_p9_buffer: std_logic;

signal ack_set:   std_logic;
signal ack_reset: std_logic;

signal sendiline_set:   std_logic;
signal sendiline_reset: std_logic;

begin

p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p8: control_cell port map (Ri_p8, Ai_p8, Ro_p8, Ao_p8);
p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p9: control_cell port map (Ri_p9, Ai_p9, Ro_p9, Ao_p9);
p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);
buffer_1: buffer_n generic map(N => 8) port map (Ro_p9, Ro_p9_buffer);

ack_cell: output_cell port map (ack_set, ack_reset, ack);
sendiline_cell: output_cell port map (sendiline_set, sendiline_reset, sendiline);

Ri_p6 <= not (not req and not ackline and (Ro_p4));
Ri_p1 <= not (reset or (Ro_p6));
Ri_p8 <= not (not ackline and (Ro_Paux1));
Ri_p2 <= not (req and (Ro_p1));
Ri_p9 <= not (not done and ackline and (Ro_p2 or Ro_p8));
Ri_p4 <= not (done and ackline and (Ro_p2 or Ro_p8));

Ri_Paux1 <= not (Ro_p9_buffer and Ai_Paux1);

Ai_p6 <= not reset and (Ao_p1);
Ai_p1 <= (Ao_p2);
Ai_p8 <= not reset and (Ao_p4 and Ao_p9);
Ai_p2 <= not reset and (Ao_p4 and Ao_p9);
Ai_p9 <= not reset and (Ao_Paux1);
Ai_p4 <= not reset and (Ao_p6);

Ai_Paux1 <= not reset and (Ao_p8);

ack_set <= (not((Ro_p4)) or not ack_reset);
ack_reset <= not reset and (not((Ro_p6)));

sendiline_set <= (not((Ro_p2) or (Ro_p8)) or not sendiline_reset);
sendiline_reset <= not reset and (not((Ro_p4) or (Ro_p9)));

end struct;
