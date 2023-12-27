import curses
import os

def list_directory_contents(directory):
	try:
		contents = os.listdir(directory)
	except OSError:
		contents = []
	if (os.listdir(readLoc()) != os.listdir(directory)):
		contents.append("..")
	return contents

def draw_menu(stdscr, selected_row_idx, directory_contents):
	message = 7*" " + "--- Notes ---" + 7*" "
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	y = 4
	x = w //2 - len(message)//2
	stdscr.addstr(1,x,27*" ",curses.color_pair(2))
	stdscr.addstr(2,x,message,curses.color_pair(2))
	stdscr.addstr(3,x,27*" ",curses.color_pair(2))
	for i, item in enumerate(directory_contents):
		x = w//2 - len(item)//2
		y += 1
		if i == selected_row_idx:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y, x, item)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y, x, item)

	stdscr.refresh()

def printFile(stdscr, filePath):
	filename = "/".join(filePath.split("/")[-2:])
	h, w = stdscr.getmaxyx()
	top, bot = 0, h-1
	stdscr.clear()
	banner = f"{' '*4}--> {filename} <--{' '*4}"
	stdscr.addstr(0,0, banner, (curses.A_UNDERLINE | curses.color_pair(1)))
	with open(filePath) as fp:
		data = fp.read()
	arr = data.split("\n")
	if (len(arr) < h-1):
		stdscr.addstr(1,0, "\n".join(arr))
	else:
		displaydata(stdscr, "\n".join(arr[top:bot]), banner)

	key = stdscr.getch()
	while(key != ord("q")):
		key = stdscr.getch()
		if (key == curses.KEY_DOWN and bot < len(arr)-1):
			top += 1
			bot += 1
			displaydata(stdscr, "\n".join(arr[top:bot]), banner)
		elif (key == curses.KEY_UP and top > 0):
			top -= 1
			bot -= 1
			displaydata(stdscr, "\n".join(arr[top:bot]), banner)
		elif (key == ord("/")):
			q = "Find phrase: "
			p = str()
			stdscr.addstr(h-1,0,q+(" "*(w-len(q)-1)), curses.A_REVERSE)
			key = stdscr.getch()
			while (key != ord("\n")):
				key = stdscr.getch()
				if key == curses.KEY_BACKSPACE:
					if (len(q) > 13):
						q = q[0:-1]
					p = p[0:-1]
					stdscr.addstr(h-1,0,q+(" "*(w-len(q)-1)), curses.A_REVERSE)
				if (key > 31 and key < 126):
					q+=chr(key)
					p+=chr(key)
					if (len(q) < w):
						stdscr.addstr(h-1,0,q+(" "*(w-len(q)-1)), curses.A_REVERSE)
			newarr = []
			for i in arr:
				if p in i:
					newarr.append(i)
			arr = newarr
			displaydata(stdscr, "\n".join(arr[0:h-1]), banner)



def displaydata(stdscr, data, banner):
	stdscr.clear()
	stdscr.addstr(0,0, banner, (curses.A_UNDERLINE | curses.color_pair(1)))
	stdscr.addstr(1,0, data)

def readLoc():
	with open("defautlnotes.location") as fp:
		data = fp.read()

	return data