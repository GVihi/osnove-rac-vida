from cv2 import cv2
import numpy as np
from numpy import asarray
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
    #Converts image into numpy array
    imgArray = asarray(img).tolist()
    #Loop through the imageArray
    for x in range(len(imgArray)):
        for y in range(len(imgArray[x])):
            r = imgArray[x][y][0]
            g = imgArray[x][y][1]
            b = imgArray[x][y][2]
            #If r,g,b values are different from one another, the image is colored
            if b != g != r:
                return False
    return True

def calculateHistogram(img):
    #Check if image is gray
    if isGray(img) == True:
        #Converts image into numpy array
        imgArray = asarray(img).tolist()
        #Array of size 256, every value set to 0
        histogram = [0] * 256
        #Loop through the imageArray
        for x in range(len(imgArray)):
            for y in range(len(imgArray[x])):
                histogram[imgArray[x][y][0]] += 1
                histogram[imgArray[x][y][1]] += 1 #Should be histogram[imgArray[x][y]] += 1 , but I think due to some cv2 grayscale error it doesn't work: 
                histogram[imgArray[x][y][2]] += 1                                      # TypeError: list indices must be integers or slices, not list

    else:
        im = Image.fromarray(img) #Constructs a CASA image from a numerical array
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order

        imgArray = asarray(im).tolist()
        rHistogram = [0] * 256
        gHistogram = [0] * 256
        bHistogram = [0] * 256

        for x in range(len(imgArray)):
            for y in range(len(imgArray[x])):
                for k in range(len(imgArray[x][y])):
                    #0: Red panel
                    if k == 0:
                        rHistogram[imgArray[x][y][k]] += 1
                    #1: Green panel
                    if k == 1:
                        gHistogram[imgArray[x][y][k]] += 1
                    #2: Blue panel
                    if k == 2:
                        bHistogram[imgArray[x][y][k]] += 1
    
    #Defined y axis on histogram
    y = np.arange(256)
    if isGray(img) == True:
        #Adding the value to be displayed in the histogram
        plt.title("Histogram - Gray")
        plt.bar(y, histogram, color = "gray")
        plt.show()
    else:
        plt.title("Histogram - Colored")
        plt.bar(y, rHistogram, color = "red")
        plt.bar(y, gHistogram, color = "green")
        plt.bar(y, bHistogram, color = "blue")
        plt.show()




def equalizeHistogram(img):
    #Check if image is gray -- copy-paste from calculatehistogram
    if isGray(img) == True:
        #Converts image into numpy array
        imgArray = asarray(img).tolist()
        #Array of size 256, every value set to 0
        histogram = [0] * 256
        #Loop through the imageArray
        for x in range(len(imgArray)):
            for y in range(len(imgArray[x])):
                histogram[imgArray[x][y][0]] += 1
                histogram[imgArray[x][y][1]] += 1 #Should be histogram[imgArray[x][y]] += 1 , but I think due to some cv2 grayscale error it doesn't work: 
                histogram[imgArray[x][y][2]] += 1                                      # TypeError: list indices must be integers or slices, not list
        
        eqHistogram = [0] * 256
        #eq Algorithm
        #[1 2 1 3 4] turns into [1 3 4 7 11]
        #Value on first index always stays the same
        eqHistogram[0] = histogram[0]
        for i in range(255):
            eqHistogram[i + 1] = histogram[i + 1] + eqHistogram[i]

    else:
        im = Image.fromarray(img) #Constructs a CASA image from a numerical array
        b, g, r = im.split() #OpenCV uses BGR order instead of RGB
        im = Image.merge("RGB", (r, g, b)) #Merging in the correct R G B order

        imgArray = asarray(im).tolist()
        rHistogram = [0] * 256
        gHistogram = [0] * 256
        bHistogram = [0] * 256

        for x in range(len(imgArray)):
            for y in range(len(imgArray[x])):
                for k in range(len(imgArray[x][y])):
                    #0: Red panel
                    if k == 0:
                        rHistogram[imgArray[x][y][k]] += 1
                    #1: Green panel
                    if k == 1:
                        gHistogram[imgArray[x][y][k]] += 1
                    #2: Blue panel
                    if k == 2:
                        bHistogram[imgArray[x][y][k]] += 1

        ReqHistogram = [0] * 256
        GeqHistogram = [0] * 256
        BeqHistogram = [0] * 256

        ReqHistogram[0] = rHistogram[0]
        GeqHistogram[0] = gHistogram[0]
        BeqHistogram[0] = bHistogram[0]

        for i in range(255):
            ReqHistogram[i + 1] = rHistogram[i + 1] + ReqHistogram[i]
            GeqHistogram[i + 1] = gHistogram[i + 1] + GeqHistogram[i]
            BeqHistogram[i + 1] = bHistogram[i + 1] + BeqHistogram[i]

    #Defined y axis on histogram -- copy-paste from calculateHistogram
    y = np.arange(256)
    if isGray(img) == True:
        #Adding the value to be displayed in the histogram
        plt.title("Equalized - Gray")
        plt.bar(y, eqHistogram, color = "gray")
        plt.show()
    else:
        plt.title("Equalized - Colored")
        plt.bar(y, ReqHistogram, color = "red")
        plt.bar(y, GeqHistogram, color = "green")
        plt.bar(y, BeqHistogram, color = "blue")
        plt.show()

def backProjection():
    something = 1


#Button1 Function -- setting file_path to whatever you choose in the openFileDialog
#Calling mainProgram function after setting file_path
def selectImage(): #Works with jpg, doesnt work with png: "AttributeError: 'NoneType' object has no attribute '__array_interface__'", whatever that means
    #openFileDialog. User selects image to display
    file_path = filedialog.askopenfilename(filetypes=[("JPG", "*.jpg *.jpeg")])

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
    command=lambda: calculateHistogram(img) #Onclick call calculateHistogram function
    )

    eqHisto = tk.Button(
    text="Equalize histogram",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=lambda: equalizeHistogram(img) #Onclick call equalizeHistogram function
    )

    backProj = tk.Button(
    text="Back projection",
    width=25,
    height=5,
    bg="yellow",
    fg="black",
    command=lambda: backProjection #Onclick call backProjection function
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