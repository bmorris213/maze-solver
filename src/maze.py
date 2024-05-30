# Maze Solver
# 05-29-24
# Brian Morris

import time
import random
from window import Window, Point, Line

ANIMATION_DELAY = 0.05

# Cell
# Represents one 'block' in a grid
class Cell():
    def __init__(self, win, a, b):
        self.left = True
        self.right = True
        self.up = True
        self.down = True
        self.win = win
        self._x1 = a.x
        self._y1 = a.y
        self._x2 = b.x
        self._y2 = b.y
        self.visited = False
    
    def draw(self):
        if self.up == True:
            self.win.draw_line( Line( Point(self._x1, self._y2), Point(self._x2, self._y2) ), Window.DRAW_COLOR )
        if self.down == True:
            self.win.draw_line( Line( Point(self._x1, self._y1), Point(self._x2, self._y1) ), Window.DRAW_COLOR )
        if self.left == True:
            self.win.draw_line( Line( Point(self._x1, self._y1), Point(self._x1, self._y2) ), Window.DRAW_COLOR )
        if self.right == True:
            self.win.draw_line( Line( Point(self._x2, self._y1), Point(self._x2, self._y2) ), Window.DRAW_COLOR )
    
    def draw_move(self, to_cell, undo=False):
        color = Window.UNDO_COLOR
        if undo == False:
            color = Window.SOLUTION_COLOR
        center = (self._x1 + self._x2) // 2
        center = Point(center, (self._y1 + self._y2) // 2)
        new_center = (to_cell._x1 + to_cell._x2) // 2
        new_center = Point(new_center, (to_cell._y1 + to_cell._y2) // 2)
        self.win.draw_line( Line(center, new_center), color )

    def erase_wall(self, direction):
        if direction == "up":
            self.up = False
            self.win.draw_line( Line( Point(self._x1, self._y1), Point(self._x2, self._y1) ), Window.BACKGROUND_COLOR )
        elif direction == "down":
            self.down = False
            self.win.draw_line( Line( Point(self._x1, self._y2), Point(self._x2, self._y2) ), Window.BACKGROUND_COLOR )
        elif direction == "left":
            self.left = False
            self.win.draw_line( Line( Point(self._x1, self._y1), Point(self._x1, self._y2) ), Window.BACKGROUND_COLOR )
        elif direction == "right":
            self.right = False
            self.win.draw_line( Line( Point(self._x2, self._y1), Point(self._x2, self._y2) ), Window.BACKGROUND_COLOR )
# Maze
# represents every cell in the maze
class Maze():
    def __init__(self, win, map_height=700, map_width=500, cell_size=50, seed=None):
        self.row_count = map_height // cell_size
        self.collumn_count = map_width // cell_size
        self.win = win
        self.entrance = (0, 0)
        self.exit = (self.collumn_count - 1, self.row_count - 1)
        if seed != None:
            random.seed(seed)

        # fill in grid
        self.maze_map = []
        for i in range(self.collumn_count):
            cells = []
            for j in range(self.row_count):
                new_x = (j * cell_size) + (cell_size // 2)
                new_y = (i * cell_size) + (cell_size // 2)
                upper_left = Point(new_x, new_y)
                lower_right = Point(new_x + cell_size, new_y + cell_size)
                cells.append(Cell(win, upper_left, lower_right))
            self.maze_map.append(cells)
    
    def draw(self):
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[i])):
                self.maze_map[i][j].draw()

    def animate(self):
        self.win.redraw()
        time.sleep(ANIMATION_DELAY)
    
    def generate_exits(self):
        directions = ["up", "down", "left", "right"]
        
        # choose random direction for entrance
        rand_dir = random.choice(directions)
        
        # carve entrance
        if rand_dir == "up":
            directions.remove("up")
            y = 0
            x = random.randrange(0, self.row_count)
            self.entrance = (x, y)
            self.maze_map[y][x].erase_wall("up")
        elif rand_dir == "down":
            directions.remove("down")
            y = self.collumn_count - 1
            x = random.randrange(0, self.row_count)
            self.entrance = (x, y)
            self.maze_map[y][x].erase_wall("down")
        elif rand_dir == "left":
            directions.remove("left")
            x = 0
            y = random.randrange(0, self.collumn_count)
            self.entrance = (x, y)
            self.maze_map[y][x].erase_wall("left")
        elif rand_dir == "right":
            directions.remove("right")
            x = self.row_count - 1
            y = random.randrange(0, self.collumn_count)
            self.entrance = (x, y)
            self.maze_map[y][x].erase_wall("right")

        # choose random direction for exit
        rand_dir = random.choice(directions)

        # carve exit
        if rand_dir == "up":
            y = 0
            x = random.randrange(0, self.row_count)
            self.exit = (x, y)
            self.maze_map[y][x].erase_wall("up")
        elif rand_dir == "down":
            y = self.collumn_count - 1
            x = random.randrange(0, self.row_count)
            self.exit = (x, y)
            self.maze_map[y][x].erase_wall("down")
        elif rand_dir == "left":
            x = 0
            y = random.randrange(0, self.collumn_count)
            self.exit = (x, y)
            self.maze_map[y][x].erase_wall("left")
        elif rand_dir == "right":
            x = self.row_count - 1
            y = random.randrange(0, self.collumn_count)
            self.exit = (x, y)
            self.maze_map[y][x].erase_wall("right")
    
    def break_walls(self):
        # generate random exits
        self.generate_exits()

        # start recursive function with start block
        self.break_walk(0, 0)

        # flip all visited status
        for i in range(self.collumn_count):
            for j in range(self.row_count):
                self.maze_map[i][j].visited = False
    
    def break_walk(self, i, j):
        # visit current cell
        self.maze_map[i][j].visited = True

        # depth first traversal
        while(True):
            possible_directions = []
            # check down
            if i > 0:
                if self.maze_map[i - 1][j].visited == False:
                    possible_directions.append("down")
            # check up
            if i < self.collumn_count - 1:
                if self.maze_map[i + 1][j].visited == False:
                    possible_directions.append("up")
            # check left
            if j > 0:
                if self.maze_map[i][j - 1].visited == False:
                    possible_directions.append("left")
            # check right
            if j < self.row_count - 1:
                if self.maze_map[i][j + 1].visited == False:
                    possible_directions.append("right")
            
            if len(possible_directions) == 0:
                return
            
            random_direction = random.randrange(0, len(possible_directions))
            for k in range(len(possible_directions)):
                if k == random_direction:
                    if possible_directions[k] == "up":
                        self.maze_map[i][j].erase_wall("down")
                        self.maze_map[i + 1][j].erase_wall("up")
                        self.break_walk(i + 1, j)
                    elif possible_directions[k] == "down":
                        self.maze_map[i][j].erase_wall("up")
                        self.maze_map[i - 1][j].erase_wall("down")
                        self.break_walk(i - 1, j)
                    elif possible_directions[k] == "right":
                        self.maze_map[i][j].erase_wall("right")
                        self.maze_map[i][j + 1].erase_wall("left")
                        self.break_walk(i, j + 1)
                    elif possible_directions[k] == "left":
                        self.maze_map[i][j].erase_wall("left")
                        self.maze_map[i][j - 1].erase_wall("right")
                        self.break_walk(i, j - 1)
    
    def solve(self, i=None, j=None):
        if i == None and j == None:
            j, i = self.entrance
        
        # visit current cell
        self.maze_map[i][j].visited = True

        # check for solution
        if i == self.exit[1] and j == self.exit[0]:
            return True
        
        directions = [ "up", "down", "left", "right" ]
        # check each direction
        for k in range(len(directions)):
            new_i = i
            new_j = j
            # check direction can be walked
            if directions[k] == "up":
                if self.maze_map[i][j].down == True:
                    continue
                if i == self.collumn_count - 1:
                    continue
                if self.maze_map[i + 1][j].visited == True:
                    continue
                new_i += 1
            elif directions[k] == "down":
                if self.maze_map[i][j].up == True:
                    continue
                if i == 0:
                    continue
                if self.maze_map[i - 1][j].visited == True:
                    continue
                new_i -= 1
            elif directions[k] == "left":
                if self.maze_map[i][j].left == True:
                    continue
                if j == 0:
                    continue
                if self.maze_map[i][j - 1].visited == True:
                    continue
                new_j -= 1
            elif directions[k] == "right":
                if self.maze_map[i][j].right == True:
                    continue
                if j == self.row_count - 1:
                    continue
                if self.maze_map[i][j + 1].visited == True:
                    continue
                new_j += 1

            # move to new direction
            self.maze_map[i][j].draw_move(self.maze_map[new_i][new_j])
            self.animate()
            solution_found = self.solve(new_i, new_j)
            if solution_found == True:
                return True
            else:
                self.maze_map[i][j].draw_move(self.maze_map[new_i][new_j], True)
                self.animate()
        
        # no direction worked out
        return False

