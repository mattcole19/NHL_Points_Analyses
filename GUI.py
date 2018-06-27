from tkinter import *
from tkinter import ttk
import pandas as pd
import pandastable as table
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#asdafaf
print()

class App():

    def __init__(self, master):
        frame = ttk.Frame(master)
        self.values = ['a', 'b', 'c']

        #x axis dropdown
        self.x = StringVar()
        self.x_combo = ttk.Combobox(frame, textvariable = self.x)
        self.x_combo.config(values = self.values)
        self.x_combo.pack()

        #y axis dropdown
        self.y = StringVar()
        self.y_combo = ttk.Combobox(frame, textvariable=self.y)
        self.y_combo.config(values=self.values)
        self.y_combo.pack()

        # hit button to create graph
        self.enter = ttk.Button(frame, text='Enter')
        self.enter.pack()
        self.enter.config(command= self.create_graph)

        fig = Figure()
        ax = fig.add_subplot(111)

        frame.pack()

    #creates and shows graph when 'enter' is pressed
    def create_graph(self):
        x_axis = self.x.get()
        y_axis = self.y.get()





#creates dataframe from csv file
df = pd.read_csv('nhl_data.csv')
print(df)


#create app and run it
root = Tk()
app = App(root)
root.mainloop()