---------------------------------------------
-- Control Cell
-- by Felipe Mendes dos Santos, 26/10/2016
--
-- Control cell is the basic component in
-- direct mapping of the asynchronous
-- controller in XSTG to the final circuit
---------------------------------------------

library ieee ;
use ieee.std_logic_1164.all;
use work.all;

---------------------------------------------

entity control_cell is
port(Ri:    in std_logic;
  Ai: in std_logic;
  Ro: inout std_logic;
  Ao: out std_logic
);
end control_cell;

----------------------------------------------

architecture behv of control_cell is
begin
Ao <= not Ro;
    process(Ai, Ri)
    begin

        -- clock rising edge
      if (Ai = '0') then
        Ro <= '0';
      elsif (Ri='0' and Ri'event) then
        Ro <= '1';
      end if;

    end process;

end behv;
