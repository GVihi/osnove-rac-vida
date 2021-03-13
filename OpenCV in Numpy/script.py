from cv2 import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time
from PIL import Image, ImageTk

#GitHub Repository URL: https://github.com/GVihi/osnove-rac-vida/tree/main/OpenCV%20in%20Numpy

save_to_disk = 0
play = 1
ff = 0

def pauseV():
    global play
    play = 0

def resumeV():
    global play
    play = 1

def fForward():
    global ff
    ff = 1

def fForward2():
    global ff
    ff = 2

def saveVideoToDisk():
    global save_to_disk
    save_to_disk = 1

#Button1 Function -- setting file_path to whatever you choose in the openFileDialog
#Calling mainProgram function after setting file_path
def selectImage(): #Works with jpg, doesnt work with png: "AttributeError: 'NoneType' object has no attribute '__array_interface__'", whatever that means
    file_path = filedialog.askopenfilename()
    button1.destroy()
    button2.destroy()
    button3.destroy()

    root.update()

    cap = cv2.VideoCapture(file_path) #"Video" source is file_path

    _, img = cap.read()

    img = cv2.resize(img, (960, 540)) #Resizing to fit screen; unmodified is too large
    #cv2.imshow('Hello', img) #Opens windows and display video/image
    while True:
        im = Image.fromarray(img)
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order
        imgtk = ImageTk.PhotoImage(image=im)
        frameImg = tk.Label(root, image=imgtk)
        frameImg.pack()
        root.update()
        frameImg.destroy()
        

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

#Button1 Function -- setting file_path to "Vid.mp4"; video file in the directory
#Calling mainProgram function after setting file_path
def selectedVideo():
    file_path = filedialog.askopenfilename()

    #Button used for pausing video
    pause = tk.Button(
    text="Pause",
    width=25,
    height=5,
    bg="red",
    fg="white",
    command=pauseV
    )

    #Button used for resuming video
    resume = tk.Button(
    text="Resume",
    width=25,
    height=5,
    bg="green",
    fg="white",
    command=resumeV
    )

    #Button used for fast forwarding video
    fast_forward = tk.Button(
    text="FF 50 Frames",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=fForward
    )

    #Button used for going back 50 frames video
    fast_forward2 = tk.Button(
    text="Rewind 50 Frames",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=fForward2
    )

    button1.destroy()
    button2.destroy()
    button3.destroy()
    pause.pack()
    resume.pack()
    fast_forward.pack()
    fast_forward2.pack()

    root.update()

    mainProgram(file_path)

#Button3 Function -- setting file_path to 0; camera feed
#Calling mainProgram function after setting file_path
def cameraFeed():
    file_path = 0

    save_video = tk.Button(
    text="Save Video",
    width=25,
    height=5,
    bg="green",
    fg="black",
    command=saveVideoToDisk
    )

    button1.destroy()
    button2.destroy()
    button3.destroy()
    save_video.pack()
    root.update()

    mainProgram(file_path)

#OpenVC function
def mainProgram(file_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 24.0, (960, 540))
    cap = cv2.VideoCapture(file_path) #"Video" source is file_path

    while True:
        global ff
        global play

        if ff == 1:
            currentPos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentPos + 50)
            ff = 0

        if ff == 2:
            currentPos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentPos - 50)
            ff = 0

        if play == 1:
            _, img = cap.read()

        img = cv2.resize(img, (960, 540)) #Resizing to fit screen; unmodified is too large
        global save_to_disk
        if save_to_disk == 1: #If save_to_disk is true, save current frame to disk
            out.write(img)

        #cv2.imshow('Hello', img) #Opens windows and display video/image
        
        im = Image.fromarray(img)
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order
        imgtk = ImageTk.PhotoImage(image=im)
        frameImg = tk.Label(root, image=imgtk)
        frameImg.pack()
        root.update()
        frameImg.destroy()

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

#Main:
#Initialize GUI
root = tk.Tk()

# --nalaganje slike iz diska v poljubnem formatu.--
button1 = tk.Button(
    text="Load Image",
    width=25,
    height=5,
    bg="blue",
    fg="white",
    command=selectImage
)

# --nalaganje video posnetka in njegovo predvajanje.--
button2 = tk.Button(
    text="Load Video",
    width=25,
    height=5,
    bg="blue",
    fg="white",
    command=selectedVideo
)

# --zajem toka iz kamere.--
button3 = tk.Button(
    text="Capture Camera",
    width=25,
    height=5,
    bg="blue",
    fg="white",
    command=cameraFeed
)

#Adding widget to window
button1.pack()
button2.pack()
button3.pack()

#Tells Python to run Tkinter "Event Loop"
root.mainloop()