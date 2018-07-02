from tkinter import *
from tkinter import ttk
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import random


'''count =0
for team in teams:
    ax.annotate(team, (x[count], y[count]))
    count+=1'''


class App():

    def __init__(self, master):
        df = pd.read_csv('nhl_data.csv')
        frame = ttk.Frame(master)
        data_frame = ttk.Frame(master)

        #title
        self.title = master.title('NHL Data Analyses')

        #header
        self.header = Label(frame, text='NHL Data Grapher', fg='red', bg='light blue', font= ('Times New Roman', 55))
        self.header.pack()

        #choose text
        self.choose = Label(frame, text='Choose the X and Y axes to see a graph comparing the variables: ')
        self.choose.pack()

        dataheader = list(df)
        #x axis dropdown
        ttk.Label(frame, text='X').pack()
        self.x = StringVar()
        self.x_combo = ttk.Combobox(frame, textvariable = self.x)
        self.x_combo.config(values = dataheader[1:])
        self.x_combo.pack()

        #y axis dropdown
        ttk.Label(frame, text='Y').pack()
        self.y = StringVar()
        self.y_combo = ttk.Combobox(frame, textvariable=self.y)
        self.y_combo.config(values= dataheader[1:])
        self.y_combo.pack()

        #hit button to create graph
        self.enter = ttk.Button(frame, text='Enter')
        self.enter.pack()
        self.enter.config(command= self.create_graph)

        frame.pack()

    #creates and shows graph when 'enter' is pressed
    def create_graph(self):
        #dataframe
        df = pd.read_csv('nhl_data.csv')
        teams = df.ix[:,0]

        #get axes
        x_axis = df[self.x.get()]
        y_axis = df[self.y.get()]

        #creates scatter plot
        ax = plt.subplot()
        ax.scatter(x_axis, y_axis)

        #puts team name next to respective marker
        count = 0
        for team in teams:
            ax.annotate(team, (x_axis[count], y_axis[count]))
            count += 1

        plt.show()



def main():
    # create app and run it
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()