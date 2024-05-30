# Maze Solver
# 05-29-24
# Brian Morris

from tkinter import Tk, BOTH, Canvas

# Point
# represents a point in a coordinate plane
class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
# Line
# represents a line between two points in a coordinate plane
class Line():
    def __init__(self, point_a=Point(), point_b=Point()):
        self.point_a = point_a
        self.point_b = point_b
    
    LINE_WIDTH = 2
    
    # Draw
    # draws current line to a given canvas and fill color
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point_a.x, self.point_a.y, self.point_b.x,
            self.point_b.y, fill=fill_color, width=self.LINE_WIDTH)

# Window
# Encapsulates graphical display for the program
class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack()
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__is_running = True

        while(self.__is_running == True):
            self.redraw()
    
    def close(self):
        self.__is_running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)