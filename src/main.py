# Maze Solver
# 05-29-24
# Brian Morris

from window import Window, Point, Line
from maze import Maze

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 50
RANDOM_SEED = None

# Main
# program begins execution here
def main():
    # create graphics window
    win = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

    # generate mazes until one has a solution
    maze_has_solution = False

    max_loop_counter = 0
    max_loop = 10

    while(maze_has_solution == False):
        max_loop_counter += 1

        maze = Maze(win, WINDOW_WIDTH - (CELL_SIZE // 10), WINDOW_HEIGHT - (CELL_SIZE // 10), CELL_SIZE, RANDOM_SEED)
        maze.draw()

        if max_loop_counter >= max_loop:
            print("Holy shit we broke it")
            break

        maze.break_walls()

        maze_has_solution = maze.solve()

    win.wait_for_close()

if __name__ == '__main__':
    main()