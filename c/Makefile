.PHONY: clean

all: tui gui

tui: board.h board.c logic.h logic.c minesweeper-tui.c
	clang -Wall -Wno-parentheses -g -O0 -o minesweeper_tui board.c logic.c minesweeper-tui.c

gui: board.h board.c logic.h logic.c minesweeper-gui.c
	clang -Wall -Wno-parentheses -g -O0 -o minesweeper_gui board.c logic.c minesweeper-gui.c

clean:
	rm -rf play test.dSYM