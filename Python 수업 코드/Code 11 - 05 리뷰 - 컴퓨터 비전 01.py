from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter import ttk
import os
import os.path
import math
import numpy
import pymysql
import csv
import xlrd
import xlwt
import xlsxwriter

window = Tk()
# window.geometry("500x500")    # geometry를 비활성화하면 canvas 크기에 따라 window 창 크기가 조절된다
window.resizable(height=True, width=False)

canvas = Canvas(window, width=500, height=500)
paper = PhotoImage(height=500, width=500)
canvas.create_image((500 // 2, 500 // 2), image=paper, state="normal")



canvas.pack(expand=1, anchor=CENTER)
window.mainloop()