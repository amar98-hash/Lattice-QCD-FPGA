library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity lqcd_top is
    generic (
        DATA_WIDTH : integer := 32
    );
    port (
        clk   : in  std_logic;
        rst   : in  std_logic;

        start : in  std_logic;
        done  : out std_logic;

        x_in  : in  std_logic_vector(DATA_WIDTH-1 downto 0);
        y_out : out std_logic_vector(DATA_WIDTH-1 downto 0)
    );
end entity lqcd_top;

architecture rtl of lqcd_top is

    type state_t is (
        IDLE,
        LOAD,
        COMPUTE,
        WRITEBACK,
        FINISH
    );

    signal state      : state_t := IDLE;
    signal x_reg      : std_logic_vector(DATA_WIDTH-1 downto 0) := (others => '0');
    signal y_reg      : std_logic_vector(DATA_WIDTH-1 downto 0) := (others => '0');
    signal cycle_count : unsigned(7 downto 0) := (others => '0');

begin

    y_out <= y_reg;

    process(clk)
    begin
        if rising_edge(clk) then

            if rst = '1' then
                state       <= IDLE;
                x_reg       <= (others => '0');
                y_reg       <= (others => '0');
                cycle_count <= (others => '0');
                done        <= '0';

            else
                done <= '0';

                case state is

                    when IDLE =>
                        cycle_count <= (others => '0');

                        if start = '1' then
                            state <= LOAD;
                        end if;

                    when LOAD =>
                        x_reg <= x_in;
                        state <= COMPUTE;

                    when COMPUTE =>
                        -- Placeholder for LQCD stencil / CG / matrix-vector core
                        -- For now, simply pass x_reg through after a few cycles.
                        cycle_count <= cycle_count + 1;

                        if cycle_count = 4 then
                            y_reg <= x_reg;
                            state <= WRITEBACK;
                        end if;

                    when WRITEBACK =>
                        state <= FINISH;

                    when FINISH =>
                        done  <= '1';
                        state <= IDLE;

                end case;
            end if;
        end if;
    end process;

end architecture rtl;