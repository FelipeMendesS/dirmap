---------------------------------------------
-- FileTest
-- by Felipe Mendes dos Santos, 26/10/2016
---------------------------------------------

library ieee ;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity FileTest is
port(reset: in std_logic;
     req: in std_logic;
     ackline: in std_logic;
     done: in std_logic;
     ack: out std_logic;
     sendline: out std_logic
);
end FileTest;

----------------------------------------------

architecture struct of FileTest is

component control_cell is
port(Ri:    in std_logic;
  Ai: in std_logic;
  Ro: inout std_logic;
  Ao: out std_logic
);
end component;

signal Ri_P1: std_logic;
signal Ai_P1: std_logic;
signal Ro_P1: std_logic;
signal Ao_P1: std_logic;

signal Ri_P2: std_logic;
signal Ai_P2: std_logic;
signal Ro_P2: std_logic;
signal Ao_P2: std_logic;

signal Ri_P4: std_logic;
signal Ai_P4: std_logic;
signal Ro_P4: std_logic;
signal Ao_P4: std_logic;

signal Ri_P6: std_logic;
signal Ai_P6: std_logic;
signal Ro_P6: std_logic;
signal Ao_P6: std_logic;

signal Ri_P7: std_logic;
signal Ai_P7: std_logic;
signal Ro_P7: std_logic;
signal Ao_P7: std_logic;

signal Ri_P9: std_logic;
signal Ai_P9: std_logic;
signal Ro_P9: std_logic;
signal Ao_P9: std_logic;

signal Ri_Paux: std_logic;
signal Ai_Paux: std_logic;
signal Ro_Paux: std_logic;
signal Ao_Paux: std_logic;

begin

P1: control_cell port map (Ri_P1, Ai_P1, Ro_P1, Ao_P1);
P2: control_cell port map (Ri_P2, Ai_P2, Ro_P2, Ao_P2);
P4: control_cell port map (Ri_P4, Ai_P4, Ro_P4, Ao_P4);
P6: control_cell port map (Ri_P6, Ai_P6, Ro_P6, Ao_P6);
P7: control_cell port map (Ri_P7, Ai_P7, Ro_P7, Ao_P7);
P9: control_cell port map (Ri_P9, Ai_P9, Ro_P9, Ao_P9);
Paux: control_cell port map (Ri_Paux, Ai_Paux, Ro_Paux, Ao_Paux);

Ri_P1 <= reset nor Ro_P9;
Ri_P2 <= not(Ro_P1 and req);
Ri_P4 <= not((Ro_Paux or Ro_P2) and (not done) and ackline);
Ri_P6 <= not(Ro_P4 and (not ackline));
Ri_P7 <= not((Ro_Paux or Ro_P2) and done and ackline);
Ri_P9 <= not(Ro_P7 and (not req) and (not ackline));
Ri_Paux <= not Ro_P6;

Ai_P1 <= Ao_P2;
Ai_P2 <= Ao_P4 and Ao_P7 and not (reset);
Ai_P4 <= Ao_P6 and not (reset);
Ai_P6 <= Ao_Paux and not (reset);
Ai_P7 <= Ao_P9 and not (reset);
Ai_P9 <= Ao_P1 and not (reset);
Ai_Paux <= Ao_P4 and Ao_P7 and not (reset);

ack <= Ro_P7 and Ao_P9;
sendline <= (Ro_P2 and Ao_P4 and Ao_P7) or (Ro_Paux and Ao_P4 and Ao_P7);

end struct;
