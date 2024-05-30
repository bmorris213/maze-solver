# Maze Solver
# 05-29-24
# Brian Morris

from window import Window
from maze import Maze

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 50
RANDOM_SEED = 0

# Main
# program begins execution here
def main():
    # create graphics window
    win = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    # generate mazes until one has a solution
    maze_has_solution = False
    while(maze_has_solution == False):
        maze = Maze(win, WINDOW_WIDTH - (CELL_SIZE // 10), WINDOW_HEIGHT - (CELL_SIZE // 10), CELL_SIZE, RANDOM_SEED)
        maze.draw()

        maze.break_walls()

        maze_has_solution = maze.solve()

    win.wait_for_close()

if __name__ == '__main__':
    main()