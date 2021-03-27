from cv2 import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

#Global variables
save_to_disk = 0
play = 1
ff = 0

#Self explanatory functions
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

def isGray(img):
    (h,w,d) = img.shape
    for i in range(w):
        for j in range(h):
            b = img[i, j, 0]
            g = img[i, j, 1]
            r = img[i, j, 2]
            if b != g != r:
                return False
    return True

def calculateHistogram(img):
    binW = (max([0, 256]) - min([0, 256])) / 3
    startBin = -0.1
    endBin = binW
    segBins = []

    i = 0
    while i < 3:
        binPair = []
        binPair.append(startBin)
        binPair.append(endBin)
        segBins.append(binPair)
        startBin += binW
        endBin += binW
        i += 1

    (h, w, d) = img.shape
    if isGray(img) == True:
        grayPanel = [[img[i, j, 0]
        for i in range(h)]
        for j in range(w)]

        histogram = [0 for i in range(3)]
        for i in range(w):
            for j in range(h):
                for k in range(3):
                    if grayPanel[i][j] > segBins[k][0] and grayPanel[i][j] < segBins[k][1]:
                        histogram[k] += 1
    else:
        rPanel = [[img[i, j, 2]
        for i in range(h)]
        for j in range(w)]
        gPanel = [[img[i, j, 1]
        for i in range(h)]
        for j in range(w)]
        bPanel = [[img[i, j, 0]
        for i in range(h)]
        for j in range(w)]

        rhistogram = [0 for i in range(3)]
        for i in range(w):
            for j in range(h):
                for k in range(3):
                    if rPanel[i][j] > segBins[k][0] and rPanel[i][j] < segBins[k][1]:
                        rhistogram[k] += 1

        ghistogram = [0 for i in range(3)]
        for i in range(w):
            for j in range(h):
                for k in range(3):
                    if gPanel[i][j] > segBins[k][0] and gPanel[i][j] < segBins[k][1]:
                        ghistogram[k] += 1

        bhistogram = [0 for i in range(3)]
        for i in range(w):
            for j in range(h):
                for k in range(3):
                    if bPanel[i][j] > segBins[k][0] and bPanel[i][j] < segBins[k][1]:
                        bhistogram[k] += 1

        #plt.hist(rhistogram)
        #plt.hist(ghistogram)
        #plt.hist(bhistogram)

        tempHist = np.array(rhistogram).reshape(-1, 1)
        y = np.arange(len(tempHist))
        plt.bar(y, tempHist[:, 0].tolist())
        tempHist = np.array(ghistogram).reshape(-1, 1)
        y = np.arange(len(tempHist))
        plt.bar(y, tempHist[:, 0].tolist())
        tempHist = np.array(bhistogram).reshape(-1, 1)
        y = np.arange(len(tempHist))
        plt.bar(y, tempHist[:, 0].tolist())
        plt.show()

    
    #(h,w,d) = img.shape
    #for i in range(h):
    #    for j in range(w):
    #        hist[img[j,i]] += 1
    #plt.plot(hist)
    #plt.show()

def equalizeHistogram():
    something = 1

def backProjection():
    something = 1


#Button1 Function -- setting file_path to whatever you choose in the openFileDialog
#Calling mainProgram function after setting file_path
def selectImage(): #Works with jpg, doesnt work with png: "AttributeError: 'NoneType' object has no attribute '__array_interface__'", whatever that means
    #openFileDialog. User selects image to display
    file_path = filedialog.askopenfilename(filetypes=[("JPG", "*.jpg")])

    #Removing "Load Image", "Load Video" and "Camera Feed" buttons
    button1.destroy()
    button2.destroy()
    button3.destroy()

    cap = cv2.VideoCapture(file_path) #"Video" source is file_path

    _, img = cap.read() #Reading frame
    #img = cv2.imread(file_path)

    #Button used for calculating histrogram
    calcHisto = tk.Button(
    text="Calculate histogram",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=lambda: calculateHistogram(img) #Onclick call ---- function
    )

    eqHisto = tk.Button(
    text="Equalize histogram",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=lambda: equalizeHistogram #Onclick call ---- function
    )

    backProj = tk.Button(
    text="Back projection",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=lambda: backProjection #Onclick call ---- function
    )

    backProj.pack(side="bottom", fill="x", expand=False)
    eqHisto.pack(side="bottom", fill="x", expand=False)
    calcHisto.pack(side="bottom", fill="x", expand=False)

    #Updating UI to show changes
    root.update()

    #hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    #plt.plot(hist)
    #plt.show()

    img = cv2.resize(img, (960, 540)) #Resizing to fit screen; unmodified is too large
    #cv2.imshow('Hello', img) #Opens windows and display video/image
    while True:
        im = Image.fromarray(img) #Constructs a CASA image from a numerical array
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order
        imgtk = ImageTk.PhotoImage(image=im) #Converts into Tkinter compatible photo image
        frameImg = tk.Label(root, image=imgtk) #Puts image into a label
        frameImg.pack() #Packs label into UI
        root.update() #Update UI to show changes
        frameImg.destroy() #Destroys every iteration, that way the frame keeps refrsehing

    cap.release() #De-allocation
    cv2.destroyAllWindows() #De-allocation
    root.quit() #Closes Tkinter UI

#Button1 Function -- setting file_path to "Vid.mp4"; video file in the directory
#Calling mainProgram function after setting file_path
def selectedVideo():
    #openFileDialog. User selects video to display
    file_path = filedialog.askopenfilename(filetypes=[("MKV", "*.mkv"), ("MP4", "*.mp4")])

    #Button used for pausing video
    pause = tk.Button(
    text="Pause",
    width=25,
    height=5,
    bg="red",
    fg="white",
    command=pauseV #Onclick call pauseV() function
    )

    #Button used for resuming video
    resume = tk.Button(
    text="Resume",
    width=25,
    height=5,
    bg="green",
    fg="white",
    command=resumeV #Onclick call resumeV() function
    )

    #Button used for fast forwarding video
    fast_forward = tk.Button(
    text="FF 50 Frames",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=fForward #Onclick call fForward2() function
    )

    #Button used for going back 50 frames video
    fast_forward2 = tk.Button(
    text="Rewind 50 Frames",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=fForward2 #Onclick call fForward2() function
    )

    #Removing "Load Image", "Load Video" and "Camera Feed" buttons
    button1.destroy()
    button2.destroy()
    button3.destroy()

    #Adding "Pause", "Resume", "Forward 50 frames" and "Back 50 frames" buttons
    pause.pack(side="bottom", fill="x", expand=False)
    resume.pack(side="bottom", fill="x", expand=False)
    fast_forward.pack(side="bottom", fill="x", expand=False)
    fast_forward2.pack(side="bottom", fill="x", expand=False)

    #Updating UI, to show changes
    root.update()

    #Calling function to display video in Window
    openCVfunction(file_path)

#Button3 Function -- setting file_path to 0; camera feed
#Calling mainProgram function after setting file_path
def cameraFeed():
    file_path = 0 #0 = Camera

    save_video = tk.Button(
    text="Save Video",
    width=25,
    height=5,
    bg="green",
    fg="black",
    command=saveVideoToDisk #Onclick call saveVideoToDisk() function
    )

    #Removing "Load Image", "Load Video" and "Camera Feed" buttons
    button1.destroy()
    button2.destroy()
    button3.destroy()

    #Adding "Save video" button
    save_video.pack(side="bottom", fill="x", expand=False)

    #Updating UI, to show changes
    root.update()

    #Calling function to display camera in Window
    openCVfunction(file_path)

#OpenVC function
def openCVfunction(file_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #Setting encoder
    out = cv2.VideoWriter('output.avi', fourcc, 24.0, (960, 540)) #File name, encoder, fps, resolution
    cap = cv2.VideoCapture(file_path) #"Video" source is file_path

    while True:
        #Telling the program to use global variables
        global ff 
        global play
        global save_to_disk

        if ff == 1:
            currentPos = cap.get(cv2.CAP_PROP_POS_FRAMES) #Get current frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentPos + 50) #Set frame to current + 50
            ff = 0 #Reset conditional variable

        if ff == 2:
            currentPos = cap.get(cv2.CAP_PROP_POS_FRAMES) #Get current frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, currentPos - 50) #Set frame to current - 50
            ff = 0 #Reset conditional variable

        if play == 1:
            _, img = cap.read() #Reading frame

        img = cv2.resize(img, (960, 540)) #Resizing to fit screen; unmodified is too large
        
        if save_to_disk == 1: #If save_to_disk is true, save current frame to disk
            out.write(img)

        #cv2.imshow('Hello', img) #Opens windows and display video/image
        
        im = Image.fromarray(img) #Constructs a CASA image from a numerical array
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order
        imgtk = ImageTk.PhotoImage(image=im) #Converts into Tkinter compatible photo image
        frameImg = tk.Label(root, image=imgtk) #Puts image into a label
        frameImg.pack() #Packs label into UI
        root.update() #Updates UI to show changes
        frameImg.destroy() #Destroys every iteration, that way the frame keeps refrsehing 

    cap.release() #De-allocation
    cv2.destroyAllWindows() #De-allocation
    root.quit() #Closes Tkinter UI

#Main:
if __name__ == "__main__":
    #Initialize GUI
    root = tk.Tk()

    # --nalaganje slike iz diska v poljubnem formatu.--
    button1 = tk.Button(
        text="Load Image",
        width=25,
        height=5,
        bg="blue",
        fg="white",
        command=selectImage #Onclick call selectImage() function
    )

    # --nalaganje video posnetka in njegovo predvajanje.--
    button2 = tk.Button(
        text="Load Video",
        width=25,
        height=5,
        bg="blue",
        fg="white",
        command=selectedVideo #Onclick call selectedVideo() function
    )

    # --zajem toka iz kamere.--
    button3 = tk.Button(
        text="Capture Camera",
        width=25,
        height=5,
        bg="blue",
        fg="white",
        command=cameraFeed #Onclick call cameraFeed() function
    )

    #Adding widget to window
    button1.pack()
    button2.pack()
    button3.pack()

    #Tells Python to run Tkinter "Event Loop"
    root.mainloop()