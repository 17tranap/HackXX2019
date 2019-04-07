#THIS IS PYTHON3
import tkinter as tk
from tkinter import *
from PIL import ImageTk
from PIL import Image #to handle non-gif image formats

import cv2
import numpy as np
from statistics import mode

import time

import random

import predict as ml

def calcSuccess(predictedCounter, randAssault):
    vidLabel.pack_forget()
    if predictedCounter == "parry_R":
        instructionLabel.config(text="RIGHT PARRY")
        if randAssault == 4 or randAssault == 2:
            descriptionLabel.config(text="You've successfully parried!")
        elif randAssault == 3:
            descriptionLabel.config(text="You've been cut!")
        elif randAssault == 5:
            descriptionLabel.config(text="You've been hit!")
        else:
            descriptionLabel.config(text="You've been grabbed!")

    if predictedCounter == "parry_L":
        instructionLabel.config(text="LEFT PARRY")
        if randAssault == 5 or randAssault == 3:
            descriptionLabel.config(text="You've successfully parried!")
        elif randAssault == 2:
            descriptionLabel.config(text="You've been cut!")
        elif randAssault == 4:
            descriptionLabel.config(text="You've been hit!")
        else:
            descriptionLabel.config(text="You've been grabbed!")

    if predictedCounter == "punch_R":
        instructionLabel.config(text="RIGHT PUNCH")
        if randAssault == 0 or randAssault == 1 or randAssault == 4:
            descriptionLabel.config(text="You've successfully counter attacked!")
        elif randAssault == 2 or randAssault == 3:
            descriptionLabel.config(text="You've been cut!")
        elif randAssault == 5:
            descriptionLabel.config(text="You've been hit!")

    if predictedCounter == "punch_L":
        instructionLabel.config(text="LEFT PUNCH")
        if randAssault == 0 or randAssault == 1 or randAssault == 5:
            descriptionLabel.config(text="You've successfully counter attacked!")
        elif randAssault == 2 or randAssault == 3:
            descriptionLabel.config(text="You've been cut!")
        elif randAssault == 4:
            descriptionLabel.config(text="You've been hit!")

    if predictedCounter == "weave_R":
        instructionLabel.config(text="RIGHT WEAVE")
        if randAssault == 1 or randAssault == 3 or randAssault == 5:
            descriptionLabel.config(text="You've successfully evaded!")
        elif randAssault == 4:
            descriptionLabel.config(text="You've been hit!")
        elif randAssault == 2:
            descriptionLabel.config(text="You've been cut!")
        else:
            descriptionLabel.config(text="You've been grabbed!")

    if predictedCounter == "weave_L":
        instructionLabel.config(text="LEFT WEAVE")
        if randAssault == 0 or randAssault == 2 or randAssault == 4:
            descriptionLabel.config(text="You've successfully evaded!")
        elif randAssault == 5:
            descriptionLabel.config(text="You've been hit!")
        elif randAssault == 3:
            descriptionLabel.config(text="You've been cut!")
        else:
            descriptionLabel.config(text="You've been grabbed!")

    if predictedCounter == "block":
        instructionLabel.config(text="BLOCK")
        if randAssault == 5 or randAssault == 4:
            descriptionLabel.config(text="You've successfully blocked!")
        elif randAssault == 2 or randAssault == 3:
            descriptionLabel.config(text="You've been cut!")
        elif randAssault == 0 or randAssault == 1:
            descriptionLabel.config(text="You've been grabbed!")
    descriptionLabel.pack()


cap = cv2.VideoCapture(0)

root = tk.Tk() #initialize tkinter by making tk rook widget--consists of window with tile bar and decoration provided by window manager. Root widget must be made first and can only be one.
root.geometry("2000x1100")

ldFrame = Frame(root).pack(side="top") #frame to hold logo and description
canvas = Canvas(ldFrame, width=700, height=200)
canvas.pack(side="top")

#open image with pil image because PhotoImage only takes gif
pilLogo = Image.open("Logo.png")
logo = ImageTk.PhotoImage(pilLogo) #makes PhotoImage from pil image
canvas.create_image(350, 100, image=logo) #adds PhotoImage to Canvas

#make basic description label from text string on the logo description frame
descriptionText = """This program trains the user to respond in self defense to common physical threats."""
descriptionLabel = tk.Label(ldFrame, justify="center", padx=10, font=("Courier", 18), wraplength=1900, text=descriptionText)
descriptionLabel.pack(side="top")

#make center frame that will show instructions initially and then have "assaulter" prompts and live video
centerFrame = Frame(root).pack()
countdownLabel = tk.Label(centerFrame, justify="center", font=("Courier", 20), text="") #invisible for now because not packed
instructionText = """In this training system, you will be prompted with how an aggressor is approaching you. You may select a difficulty for this system by choosing how much time you would like to be allowed to react. Based on your counter attack, the system will tell you if the attacker has been [Narrowly Avoided], [Stunned], or [Subdued] based on the quality of your reaction. Your success rate will be tracked at the bottom of the screen. Press the [Start] button to begin and the [Stop] button to end the session."""
instructionLabel = tk.Label(centerFrame, justify="center", padx=50, pady=50, font=("Courier", 16), wraplength=1800, text=instructionText)
instructionLabel.pack(side="top")

#setup to capture video frames
vidLabel = Label(root)
def show_frame(milliseconds):
    if milliseconds > 0:
        #global predictionArr
        _, frame = cap.read()
        #predictionArr.append(predict.get_prediction(frame, "ace-connection-236822", "ICN2459521650166688930"))
        frame = cv2.flip(frame, 1) #horizontally flips images so is like reflection
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) #makes normal color
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(img)
        vidLabel.imgtk = imgtk
        vidLabel.config(image=imgtk)
        root.update()
        root.after(30, show_frame, (milliseconds-30))
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    img = Image.fromarray(cv2image)
    img = img.convert("RGB")
    img.save("imgFile.jpeg")
    if milliseconds == secondsChosen*3000: 
        return ml.predict("imgFile.jpeg")

#make bottom frame that hold buttons
buttonFrame = Frame(root)
buttonFrame.pack(side="bottom")
difficultyList = Listbox(buttonFrame, selectmode=SINGLE, height=3, font=("Courier", 16))
difficultyList.insert(1, "Easy: 6 seconds")
difficultyList.insert(2, "Medium: 3 seconds")
difficultyList.insert(3, "Hard: 1 seconds")
difficultyList.pack(side="top")

cycling = True

def runPrompt():
    startButton.config(text="Next")
    startButton.pack(side=LEFT)
    resetButton.pack(side=RIGHT)
    descriptionLabel.pack_forget()
    assaultList = ["Grab from your right", "Grab from your left", "Blade attack from the right", "Blade attack from the left", "Hit from the right", "Hit from the left"]
    counterList = ["parry_R", "parry_L", "weave_R", "weave_L", "punch_R", "punch_L", "block"]
    difficultyChoice = (difficultyList.get(ACTIVE))
    global secondsChosen
    secondsChosen = 0
    if difficultyChoice[0] == "E":
        secondsChosen = 6
    elif difficultyChoice[0] == "M":
        secondsChosen = 3
    else:
        secondsChosen = 1
    print(secondsChosen)
    difficultyList.pack_forget()

    randAssault = random.randint(0, 5)
    instructionLabel.config(text=assaultList[randAssault], font=("Courier", 25))
    vidLabel.pack()
    
    predictedCounter = show_frame(secondsChosen*1000)
    
    if predictedCounter not in counterList:
        predictedCounter = counterList[random.randint(0, 6)]
    
    root.after(secondsChosen*1200, calcSuccess, predictedCounter, randAssault)

    return 0

def reset():
    resetButton.pack_forget()
    startButton.config(text="Start")
    startButton.pack(side=BOTTOM)
    instructionLabel.config(text=instructionText, font=("Courier", 16))
    descriptionLabel.config(text=descriptionText, font=("Courier", 18))
    descriptionLabel.pack(side=TOP)
    difficultyList.pack(side=TOP)


startButton = Button(buttonFrame, bd=6, padx=20, pady=20,font=("Courier", 16), text="Start", fg="green", command=runPrompt)
startButton.pack(side=BOTTOM)
resetButton = Button(buttonFrame, bd=6, padx=20, pady=20, font=("Courier", 16), text="Reset", fg="red", command=reset)
    

root.mainloop()
cap.release()
