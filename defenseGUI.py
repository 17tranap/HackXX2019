#THIS IS PYTHON3
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image #to handle non-gif image formats


root = tk.Tk() #initialize tkinter by making tk rook widget--consists of window with tile bar and decoration provided by window manager. Root widget must be made first and can only be one.
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()
pilLogo = Image.open("Logo.png")
logo = ImageTk.PhotoImage(pilLogo)
canvas.create_image(500, 500, image=logo)
instructionText = """This program trains the user to respond in self defense to common physical threats."""
instructionLabel = tk.Label(root, justify="center", padx=10, font=("Courier", 36), text=instructionText).pack(side="top")
#canvas.create_text(0, 0, anchor=CENTER, text=instructionText) #0,0 position must be given but will be overridden by anchor
root.mainloop()


