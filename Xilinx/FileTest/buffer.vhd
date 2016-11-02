----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    12:42:35 11/02/2016 
-- Design Name: 
-- Module Name:    buffer - Behavioral 
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

entity buffer_n is
	generic (N: integer := 4);
    Port ( a : in  STD_LOGIC;
           b : out  STD_LOGIC);
end buffer_n;

architecture Behavioral of buffer_n is
signal S: std_logic_vector(0 to N);
attribute keep:string;
attribute keep of S: signal is "true";
begin
	S(0) <= a;
	buff: for i in 1 to N generate
		S(i) <= not S(i-1);
	end generate;
	b <= S(N);
end Behavioral;

