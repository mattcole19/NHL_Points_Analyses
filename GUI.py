from tkinter import *
from tkinter import ttk
import pandas as pd
import pandastable as table
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class App():

    def __init__(self, master):
        frame = ttk.Frame(master)
        self.values = ['POINTS', 'W', 'GF']

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

        frame.pack()

    #creates and shows graph when 'enter' is pressed
    def create_graph(self):
        #dataframe
        df = pd.read_csv('nhl_data.csv')

        #get axes
        x_axis = self.x.get()
        y_axis = self.y.get()

        #creates scatter plot
        scatter = df.plot.scatter(x= x_axis, y= y_axis , s= 50, c= 'DarkBlue')
        plt.show()

        #create figure for graph
        fig = Figure()
        ax = fig.add_subplot(111)







def main():
    # create app and run it
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()