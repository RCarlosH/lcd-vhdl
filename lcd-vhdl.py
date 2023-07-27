

prog = ('''--LCD: System that displays a text on the liquid crystal display of the DE2 development board
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity LCD is
 port(CLK50, SW:in std_logic; --CLOCK_50 and a SW
      RS,RW,EN,LCD_ON,LCD_BLON:out std_logic; --LCD pins (the name is similar)
      DATA:out integer range 0 to 255); --LCD_DATA pins
end entity;

architecture arq of LCD is
signal c:integer range 0 to 50000000;
signal clk: std_logic;
signal edo_act,edo_sig: integer range 0 to 102;
 begin
 LCD_ON<='1'; 
 LCD_BLON<='0';--check, could be a '1'
  process(CLK50,SW)
    begin
    if (SW='1') then
    clk<='0';c<=0;
    elsif (rising_edge(CLK50))then
      c<=c+1;
       if(c=7000)then
         c<=0;clk<=not clk;
       end if;
    end if;
  end process;

 process(edo_act)
 begin
 case edo_act is
  when  0=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=1;--Function set 8 bits 1
  when  1=>RS<='0'; RW<='0'; EN<='1'; DATA<=56;  edo_sig<=2;
  when  2=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=3;

  when  3=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=4;--Function set 8 bits 2
  when  4=>RS<='0'; RW<='0'; EN<='1'; DATA<=56;  edo_sig<=5;
  when  5=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=6;

  when  6=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=7;--Function set 8 bits 3
  when  7=>RS<='0'; RW<='0'; EN<='1'; DATA<=56;  edo_sig<=8;
  when  8=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=9;

  when  9=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=10;--Function set 2 lines 5x7
  when 10=>RS<='0'; RW<='0'; EN<='1'; DATA<=56;  edo_sig<=11;
  when 11=>RS<='0'; RW<='0'; EN<='0'; DATA<=56;  edo_sig<=12;

  when 12=>RS<='0'; RW<='0'; EN<='0'; DATA<=12;  edo_sig<=13;--Display on
  when 13=>RS<='0'; RW<='0'; EN<='1'; DATA<=12;  edo_sig<=14;
  when 14=>RS<='0'; RW<='0'; EN<='0'; DATA<=12;  edo_sig<=15;

  when 15=>RS<='0'; RW<='0'; EN<='0'; DATA<=1;   edo_sig<=16;--Display clear
  when 16=>RS<='0'; RW<='0'; EN<='1'; DATA<=1;   edo_sig<=17;
  when 17=>RS<='0'; RW<='0'; EN<='0'; DATA<=1;   edo_sig<=18;

  when 18=>RS<='0'; RW<='0'; EN<='0'; DATA<=6;   edo_sig<=19;--Entry mode set
  when 19=>RS<='0'; RW<='0'; EN<='1'; DATA<=6;   edo_sig<=20;
  when 20=>RS<='0'; RW<='0'; EN<='0'; DATA<=6;   edo_sig<=21;
  ''')

txt = input('Text to display on the screen: ')

over = 0
pos_last = int()
stat = 0
for pos in range(len(txt)):
  over = 3
  if pos == 15:
    prog = prog + f"\n  when {21+stat}=>RS<='1'; RW<='0'; EN<='0'; DATA<=192; edo_sig<={22+stat}; --Line Break\n"
    prog = prog + f"  when {22+stat}=>RS<='1'; RW<='0'; EN<='1'; DATA<=192; edo_sig<={23+stat};\n"
    prog = prog + f"  when {23+stat}=>RS<='1'; RW<='0'; EN<='0'; DATA<=192; edo_sig<={24+stat};\n"
    
    stat += 3

  prog = prog + f"\n  when {21+stat}=>RS<='1'; RW<='0'; EN<='0'; DATA<={ord(txt[pos])}; edo_sig<={22+stat}; --{txt[pos]}\n"
  prog = prog + f"  when {22+stat}=>RS<='1'; RW<='0'; EN<='1'; DATA<={ord(txt[pos])}; edo_sig<={23+stat};\n"
  prog = prog + f"  when {23+stat}=>RS<='1'; RW<='0'; EN<='0'; DATA<={ord(txt[pos])}; edo_sig<={24+stat};\n"
  
  pos_last = stat
  
  stat += over

prog += (f'''
  when {pos_last+24}=>RS<='0';RW<='0';EN<='0';DATA<=0;edo_sig <= 0;--Anchor				
  when others =>RS<='0';RW<='0';EN<='0';DATA<=0;edo_sig<=0;--others
 end case;
 end process;

process(clk)
  begin
   if (rising_edge(clk)) then edo_act <= edo_sig; end if;
 end process;
end architecture;''')

print(prog)

with open('arq.vhdl', 'w') as out:
  out.write(prog)
