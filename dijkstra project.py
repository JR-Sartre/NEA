import tkinter as tk
import time
import math
from  import Image



root = tk.Tk()
root.title("Dijkstra project")
root.eval("tk::PlaceWindow . center")

frame1 = tk.Frame(root,width= 500,height=600,bg="blue")
frame1.grid(row=0, column=0)

testbutton = tk.Button(root, text = 'hey dude', fg = 'red')
testbutton.grid(row=1,column=0)



root.mainloop()
