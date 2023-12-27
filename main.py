#!/usr/bin/python3.11
import os
import curses
import sidefunctions as sf

notesdir = sf.readLoc()

def main(stdscr, directory):
	curses.curs_set(0)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_CYAN)
	stdscr.timeout(100)  # Set a timeout for getch() to make it non-blocking

	current_row = 0
	directory_contents = sf.list_directory_contents(directory)

	while True:
		sf.draw_menu(stdscr, current_row, directory_contents)

		key = stdscr.getch()

		if key == curses.KEY_UP:
			if current_row > 0:
				current_row -= 1
			else:
				current_row = len(directory_contents) - 1
		elif key == curses.KEY_DOWN:
			if current_row < len(directory_contents) - 1:
				current_row += 1
			else:
				current_row = 0
		elif key == ord("\n"):
			if (os.path.isdir(directory+"/"+directory_contents[current_row])):
				directory = directory+"/"+directory_contents[current_row]
				current_row = 0
				directory_contents = sf.list_directory_contents(directory)
			else:
				sf.printFile(stdscr, directory+"/"+directory_contents[current_row])
		elif key == 27 or key == ord("q"):  # ESC key to exit
			break

if __name__ == "__main__":
	curses.wrapper(main, notesdir)
