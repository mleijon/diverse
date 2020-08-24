import numpy as np
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTk, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
def on_key_event(event):
   print('you pressed %s'%event.key)
   key_press_handler(event, canvas, toolbar)
def mOpen():
   var = IntVar()
   slider_1 = Scale(mGui,orient=HORIZONTAL,length = 100,from_=0,to=9,variable=var)
   slider_1.place(x = 765,y=390)
   t = np.arange(100000).reshape(100,100,10)
   f = Figure(figsize=(5,4),dpi=100)
   a = f.add_subplot(111)
   a.imshow(t[:,:,var.get()])
   print(var.get())
   canvas_3 = FigureCanvasTk(f,master = mGui)
   canvas_3.show()
   canvas_3.get_tk_widget().place(x=5,y=5)
   toolbar_3 = NavigationToolbar2Tk( canvas_3, mGui )
   toolbar_3.update()
   toolbar_3.place(x=10,y=15)
   canvas_3._tkcanvas.place(x=7,y=7)
   canvas_3.mpl_connect('key_press_event', on_key_event)
mGui = Tk()
mOpen()
mGui.geometry('900x900+300+10')
mGui.title('Plot')
mGui.mainloop()