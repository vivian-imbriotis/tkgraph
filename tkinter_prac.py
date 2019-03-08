import tkinter as tk
import time as t
from math import sin
from functools import partial
from time import sleep


def gen_xy_sample(func, low_bound, high_bound, step_size):
    if not callable(func):
        raise TypeError("func must be a callable function!")
    output = []
    for x in range(low_bound, high_bound+step_size,step_size):
        y = func(x)
        output.append((x,y))
    return output
        

class Grapher:
    def __init__(self):
        self.xres = 800
        self.yres = 600
        self.x_max = 100
        self.y_max = 100
        self.root = tk.Tk()
        self.can = tk.Canvas(self.root, width = self.xres,
                             height = self.yres)
        self.x_axis = None
        self.y_axis = None
        self.refresh()

    def coord_to_pixel(self,point):
        x,y = point
        x = self.xres* (0.5 + (x / self.x_max))
        y = self.yres* (0.5 + (y / self.y_max))
        return (x,y)

    def refresh(self):
        self.can.pack()
        self.root.update()
        self.root.update_idletasks()
    
    def add_axes(self):
        self.x_axis = self.can.create_line(0, self.yres//2,
                                           self.xres,self.yres//2)
        self.y_axis = self.can.create_line(self.xres//2,0,
                                           self.xres//2,self.yres)
        self.refresh()

    def remove_axes(self):
            self.can.delete(self.x_axis)
            self.can.delete(self.y_axis)
            self.refresh()

    def graph_points(self,list_of_tuplepoints,color="black"):
        """
        List of points should be an alternating series of x,y
        points eg for points (0,1) and (17,4), input [(0,1),(17,4)]
        """
        raw_point_list = []
        for tuplepoint in list_of_tuplepoints:
            tuplepoint = self.coord_to_pixel(tuplepoint)
            for ordin in tuplepoint:
                raw_point_list.append((ordin))
        self.curve = self.can.create_line(*raw_point_list,fill=color)
    def graph_func(self,func,color="blue"):
        self.graph_points(gen_xy_sample(func,-self.x_max,self.x_max,
                                            1),color)
    def del_curve(self):
        self.can.delete(self.curve)

    def graph_tfunc(self,func,color="blue",duration=10,step_speed = 0.1):
        while True:
            for t in range(round(duration/step_speed)):
                self.graph_func(partial(func,t))
                self.refresh()
                sleep(step_speed)
                self.del_curve()


#goal: animate time-varying multivarites (eventually, show ode numerical solns)

def f(t,x):
        return 10*sin((x-t)/2) + 10*sin((x-1.2*t)/3)

g = Grapher()
g.add_axes()
g.graph_tfunc(f)


