--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   19:12:02 10/27/2016
-- Design Name:   
-- Module Name:   C:/Users/EA-282/Downloads/Felipe/testFile/testFileTest.vhd
-- Project Name:  testFile
-- Target Device:  
-- Tool versions:  
-- Description:   
-- 
-- VHDL Test Bench Created by ISE for module: FileTest
-- 
-- Dependencies:
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
-- Notes: 
-- This testbench has been automatically generated using types std_logic and
-- std_logic_vector for the ports of the unit under test.  Xilinx recommends
-- that these types always be used for the top-level I/O of a design in order
-- to guarantee that the testbench will bind correctly to the post-implementation 
-- simulation model.
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY testFileTest IS
END testFileTest;
 
ARCHITECTURE behavior OF testFileTest IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT FileTest
    PORT(
         reset : IN  std_logic;
         req : IN  std_logic;
         ackline : IN  std_logic;
         done : IN  std_logic;
         ack : OUT  std_logic;
         sendline : OUT  std_logic
        );
    END COMPONENT;
    

   --Inputs
   signal reset : std_logic := '0';
   signal req : std_logic := '0';
   signal ackline : std_logic := '0';
   signal done : std_logic := '1';

 	--Outputs
   signal ack : std_logic;
   signal sendline : std_logic;
   -- No clocks detected in port list. Replace <clock> below with 
   -- appropriate port name 
 
   --constant <clock>_period : time := 10 ns;
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: FileTest PORT MAP (
          reset => reset,
          req => req,
          ackline => ackline,
          done => done,
          ack => ack,
          sendline => sendline
        );

   -- Clock process definitions
--   <clock>_process :process
--   begin
--		<clock> <= '0';
--		wait for <clock>_period/2;
--		<clock> <= '1';
--		wait for <clock>_period/2;
--   end process;
 

   -- Stimulus process
   stim_proc: process
   begin		
      -- hold reset state for 100 ns.
		reset <= '1';
      wait for 50 ns;
		reset <= '0';
		wait for 50 ns;
		reset <= '1';
		wait for 50 ns;
		reset <= '0';
		wait for 50 ns;
      -- insert stimulus here 
		
		req <= '1';
		wait for 50 ns;
		
		ackline <= '1';
		wait for 50 ns;		
		ackline <= '0';
		req <= '0';
		wait for 50 ns;		
		req <= '1';		
		done <= '0';
		wait for 50 ns;
		ackline <= '1';
		wait for 50 ns;
		ackline <= '0';
		wait for 50 ns;
		ackline <= '1';
		wait for 50 ns;
		ackline <= '0';
		wait for 50 ns;
      wait;
   end process;

END;
