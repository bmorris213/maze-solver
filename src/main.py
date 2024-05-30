# Maze Solver
# 05-29-24
# Brian Morris

from window import Window, Point, Line

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Main
# program begins execution here
# execution is passed
def main():
    # open graphics window
    win = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    START = 50

    current_width = WINDOW_WIDTH - START
    current_height = WINDOW_HEIGHT - START

    while current_width >= 0 and current_height >= 0:
        # draw top line
        win.draw_line( Line( Point(START, current_height), Point(WINDOW_WIDTH - START, current_height) ), "black" )
        # draw right line
        win.draw_line( Line( Point(current_width, START), Point(current_width, WINDOW_HEIGHT - START) ), "black" )
        current_width -= START
        current_height -= START

    win.wait_for_close()

if __name__ == '__main__':
    main()