----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    13:47:35 11/02/2016 
-- Design Name: 
-- Module Name:    output_cell - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity output_cell is
    Port ( set : in  STD_LOGIC;
           reset : in  STD_LOGIC;
           output : out  STD_LOGIC);
end output_cell;

architecture Behavioral of output_cell is

begin
    process(set, reset)
    begin

        -- clock rising edge
      if (reset = '0') then
        output <= '0';
      elsif (set='0' and set'event) then
        output <= '1';
      end if;

    end process;


end Behavioral;

