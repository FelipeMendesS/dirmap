---------------------------------------------
-- testFile
-- by Felipe Mendes dos Santos, 04/11/2016
---------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity testFile is
port(reset :in  std_logic;
     done:     in  std_logic;
     ackline:  in  std_logic;
     req:      in  std_logic;
     sendline: out std_logic;
     ack:      out std_logic);
end testFile;

---------------------------------------------

architecture struct of testFile is

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

signal Ri_p4: std_logic;
signal Ai_p4: std_logic;
signal Ro_p4: std_logic;
signal Ao_p4: std_logic;

signal Ri_p1: std_logic;
signal Ai_p1: std_logic;
signal Ro_p1: std_logic;
signal Ao_p1: std_logic;

signal Ri_p6: std_logic;
signal Ai_p6: std_logic;
signal Ro_p6: std_logic;
signal Ao_p6: std_logic;

signal Ri_p2: std_logic;
signal Ai_p2: std_logic;
signal Ro_p2: std_logic;
signal Ao_p2: std_logic;

signal Ri_p7: std_logic;
signal Ai_p7: std_logic;
signal Ro_p7: std_logic;
signal Ao_p7: std_logic;

signal Ri_p9: std_logic;
signal Ai_p9: std_logic;
signal Ro_p9: std_logic;
signal Ao_p9: std_logic;

signal Ri_Paux1: std_logic;
signal Ai_Paux1: std_logic;
signal Ro_Paux1: std_logic;
signal Ao_Paux1: std_logic;

signal Ro_p6_buffer: std_logic;

signal sendline_set:   std_logic;
signal sendline_reset: std_logic;

signal ack_set:   std_logic;
signal ack_reset: std_logic;

begin

p4: control_cell port map (Ri_p4, Ai_p4, Ro_p4, Ao_p4);
p1: control_cell port map (Ri_p1, Ai_p1, Ro_p1, Ao_p1);
p6: control_cell port map (Ri_p6, Ai_p6, Ro_p6, Ao_p6);
p2: control_cell port map (Ri_p2, Ai_p2, Ro_p2, Ao_p2);
p7: control_cell port map (Ri_p7, Ai_p7, Ro_p7, Ao_p7);
p9: control_cell port map (Ri_p9, Ai_p9, Ro_p9, Ao_p9);

Paux1: control_cell port map (Ri_Paux1, Ai_Paux1, Ro_Paux1, Ao_Paux1);
buffer_1: buffer_n generic map(N => 8) port map (Ro_p6, Ro_p6_buffer);

sendline_cell: output_cell port map (sendline_set, sendline_reset, sendline);
ack_cell: output_cell port map (ack_set, ack_reset, ack);

Ri_p4 <= not (not done and ackline and (Ro_p2 or Ro_Paux1));
Ri_p1 <= not (reset or (Ro_p9));
Ri_p6 <= not (not ackline and (Ro_p4));
Ri_p2 <= not (req and (Ro_p1));
Ri_p7 <= not (done and ackline and (Ro_p2 or Ro_Paux1));
Ri_p9 <= not (not req and not ackline and (Ro_p7));

Ri_Paux1 <= not Ro_p6_buffer;

Ai_p4 <= not reset and (Ao_p6);
Ai_p1 <= (Ao_p2);
Ai_p6 <= not reset and (Ao_Paux1);
Ai_p2 <= not reset and (Ao_p4 and Ao_p7);
Ai_p7 <= not reset and (Ao_p9);
Ai_p9 <= not reset and (Ao_p1);

Ai_Paux1 <= not reset and (Ao_p4 and Ao_p7);

sendline_set <= (not((Ro_p2) or (Ro_p6)) or not sendline_reset);
sendline_reset <= not reset and (not((Ro_p7) or (Ro_p4)));

ack_set <= (not((Ro_p7)) or not ack_reset);
ack_reset <= not reset and (not((Ro_p9)));

end struct;
