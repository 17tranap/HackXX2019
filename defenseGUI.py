#THIS IS PYTHON3
import tkinter as tk
from tkinter import *
from PIL import ImageTk
from PIL import Image #to handle non-gif image formats

import cv2
import numpy as np

import random

import predict

cap = cv2.VideoCapture(0)

root = tk.Tk() #initialize tkinter by making tk rook widget--consists of window with tile bar and decoration provided by window manager. Root widget must be made first and can only be one.

ldFrame = Frame(root).pack(side="top") #frame to hold logo and description
canvas = Canvas(ldFrame, width=700, height=200)
canvas.pack(side="top")

#open image with pil image because PhotoImage only takes gif
pilLogo = Image.open("Logo.png")
logo = ImageTk.PhotoImage(pilLogo) #makes PhotoImage from pil image
canvas.create_image(350, 100, image=logo) #adds PhotoImage to Canvas

#make basic description label from text string on the logo description frame
descriptionText = """This program trains the user to respond in self defense to common physical threats."""
descriptionLabel = tk.Label(ldFrame, justify="center", padx=10, font=("Courier", 18), text=descriptionText).pack(side="top")

#make center frame that will show instructions initially and then have "assaulter" prompts and live video
centerFrame = Frame(root).pack()
countdownLabel = tk.Label(centerFrame, justify="center", font=("Courier", 20), text="") #invisible for now because not packed
instructionText = """In this training system, you will be prompted with how an aggressor is approaching you. You may select a difficulty for this system by choosing how much time you would like to be allowed to react. Based on your counter attack, the system will tell you if the attacker has been [Narrowly Avoided], [Stunned], or [Subdued] based on the quality of your reaction. Your success rate will be tracked at the bottom of the screen. Press the [Start] button to begin and the [Stop] button to end the session."""
instructionLabel = tk.Label(centerFrame, justify="center", padx=50, pady=50, font=("Courier", 16), wraplength=1800, text=instructionText)
instructionLabel.pack(side="top")

#setup to capture video frames
vidLabel = Label(root)
def show_frame(milliseconds):
    _, frame = cap.read()
    frame = cv2.flip(frame, 1) #horizontally flips images so is like reflection
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) #makes normal color
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(img)
    vidLabel.imgtk = imgtk
    vidLabel.config(image=imgtk)
    root.update()
    print(milliseconds)
    if milliseconds < 0:
        print(predict.get_prediction(frame, "ace-connection-236822", "ICN2459521650166688930"))
        return
    root.after(30, show_frame(milliseconds-30))
        

#make bottom frame that hold buttons
buttonFrame = Frame(root)
buttonFrame.pack(side="bottom")
difficultyList = Listbox(buttonFrame, selectmode=SINGLE, height=3, font=("Courier", 16))
difficultyList.insert(1, "Easy: 6 seconds")
difficultyList.insert(2, "Medium: 3 seconds")
difficultyList.insert(3, "Hard: 1 seconds")
difficultyList.pack(side="top")

cycling = True

def runPrompts():
    assaultList = ["Grab from your right", "Grab from your left", "Blade attack from the right", "Blade attack from the left", "Hit from the right", "Hit from the left"]
    difficultyChoice = (difficultyList.get(ACTIVE))
    secondsChosen = 0
    if difficultyChoice[0] == "E":
        secondsChosen = 6
    if difficultyChoice[0] == "M":
        secondsChosen = 3
    else:
        secondsChosen = 1

    #countdownLabel.config(text=str(secondsChosen))
    #countdownLabel.pack()
    while cycling:
        randAssault = random.randint(0, 5)
        instructionLabel.config(text=assaultList[randAssault], font=("Courier", 25))
        vidLabel.pack()
        difficultyList.pack_forget()
        root.update()
        
        show_frame(secondsChosen*1000)
        #countdown(secondsChosen) #here call method to analyze recording and print success
        vidLabel.pack_forget()

    difficultyList.pack()
    instructionLabel.config(text=instructionText)



    return 0

def countdown(seconds):
    countdownLabel.config(text=str(seconds))
    if seconds > 0:
        #after 1000 ms call countdown again on smaller number
        countdownLabel.after(1000, countdown, seconds-1)
    else:
        countdownLabel.config(text="")
        instructionLabel.config(text="Success")

def stopPrompts():
    global cycling
    cycling = False


startButton = Button(buttonFrame, bd=6, padx=20, pady=20,font=("Courier", 16), text="Start", fg="green", command=runPrompts).pack(side=LEFT)
stopButton = Button(buttonFrame, bd=6, padx=20, pady=20, font=("Courier", 16), text="Stop", fg="red", command=stopPrompts).pack(side=RIGHT)
    

root.mainloop()
cap.release()
