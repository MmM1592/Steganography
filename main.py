import gui
import tkinter as tk


FLAG_NUMBER = 123 #number indicating hidden message

root = tk.Tk()
app = gui.GUI(root, FLAG_NUMBER)
root.mainloop() 