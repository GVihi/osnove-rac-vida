from cv2 import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time

save_to_disk = "no"

def saveVideoToDisk():
    global save_to_disk
    save_to_disk = "yes"

#Button1 Function -- setting file_path to whatever you choose in the openFileDialog
#Calling mainProgram function after setting file_path
def selectImage():
    file_path = filedialog.askopenfilename()
    mainProgram(file_path)

#Button1 Function -- setting file_path to "Vid.mp4"; video file in the directory
#Calling mainProgram function after setting file_path
def selectedVideo():
    file_path = "Vid.mp4"

    #Button used for pausing video; TODO implementation
    pause = tk.Button(
    text="Pause",
    width=25,
    height=5,
    bg="red",
    fg="white"
    )

    #Button used for resuming video; TODO implementation
    resume = tk.Button(
    text="Resume",
    width=25,
    height=5,
    bg="green",
    fg="white"
    )

    #Button used for fast forwarding video; TODO implementation
    fast_forward = tk.Button(
    text="FF 5 Sec",
    width=25,
    height=5,
    bg="yellow",
    fg="white"
    )

    button1.destroy()
    button2.destroy()
    button3.destroy()
    pause.pack()
    resume.pack()
    fast_forward.pack()

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
    out = cv2.VideoWriter('output.avi', -1, 20.0, (640, 480))
    cap = cv2.VideoCapture(file_path) #"Video" source is file_path

    while True:
        _, img = cap.read()

        img = cv2.resize(img, (960, 540)) #Resizing to fit screen; unmodified is too large
        cv2.imshow('Hello', img) #Opens windows and display video/image
        if save_to_disk == "yes": #If save_to_disk is true, save current frame to disk
            out.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'): #Waits for input, if "q" breaks loop
            break

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

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