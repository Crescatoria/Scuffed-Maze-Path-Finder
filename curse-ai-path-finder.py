import curses
from curses import wrapper
import queue

maze = [
    "#############################################################",
    "#O    #           #       #   #       #       #     #     #",
    "# ### # ##### ### # ##### # # # ##### # ##### # ### ##### #",
    "# #   # #   #   # #   #   # # #       #     # #   #     # #",
    "# # ### ### ##### ### # ##### ######### ### # # ##### # # #",
    "# #       #     #     # #             #   #   #     # #   #",
    "# ######### ##### ##### # ########### # ##### ######### # #",
    "#       #   #     #     #       #     #     #         # # #",
    "# ##### # # # # ##### ####### # # # # # ############# # # #",
    "# #   # # #   #     #       # # #   # #   #   #   #   # # #",
    "# # # # # ##### ######### # # ##### ##### ### # # # ### #",
    "#   # #     #   #   #     # #         #     #   #   #   #",
    "##### ####### ### ### ####### ##### # ################# #",
    "#     #   #   #   #     #   #   #   #   #   #   #   #   #",
    "# ### # # # # # # ##### # # # # # # # # # # ### # # #####",
    "# #   # #   # # #   #   # #   # #   # # # #     # #     #",
    "# # ##### # # ##### # ##### # # ##### # # ######### # # #",
    "# #     # # #     # #     # # #     # # #     #     # # #",
    "# ##### # ######### # ##### # ##### # # # ##### ##### # #",
    "#     # #   #       #   #   #   #   # # #       #     # #",
    "# ### # ### ######### # ##### # ### # # ######### ##### #",
    "#   #       #   #   # # #   #     # # #         #     # #",
    "# ########### # # # # # # #       # # ############# # # #",
    "#   #     #   #   #   #   #   #   # #               # # #",
    "# # # # # ######### # ######### ### ################# # #",
    "# #   # #     #   #   #     #                           #",
    "# ### # ##### # ######### ####### #################X#####",
    "#   #       # #       #     #   #                         ",
    "#############################################################",
]

# Adjust the scale factor and cell spacing
SCALE_FACTOR = 1
CELL_SPACING = 0

def print_maze(stdscr, maze, path=[]):
    stdscr.clear()
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j, "X", curses.color_pair(2))
            else:
                stdscr.addstr(i, j, value + " " * CELL_SPACING, curses.color_pair(1))
    stdscr.refresh()

def find_start_end(maze):
    start, end = None, None
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == "O":
                start = (i, j)
            elif value == "X":
                end = (i, j)
    return start, end

def find_path(maze, stdscr):
    start, end = find_start_end(maze)

    q = queue.Queue()
    q.put((start, [start]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        if current_pos == end:
            return path

        if current_pos in visited:
            continue

        visited.add(current_pos)

        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for neighbor in neighbors:
            r, c = neighbor
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != "#":
                new_path = path + [(r, c)]
                q.put(((r, c), new_path))
                print_maze(stdscr, maze, new_path)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    path = find_path(maze, stdscr)

    if path:
        stdscr.addstr(len(maze), 0, "Path found!")
    else:
        stdscr.addstr(len(maze), 0, "No path found!")

    stdscr.getch()

wrapper(main)
