import cv2 as cv
import pyvirtualcam
import numpy as np
import win32api
import pathlib
from threading import Thread 

# Constants
IMG_W = 640
IMG_H = 480
WM_APPCOMMAND = 0x319
APPCOMMAND_MIC_MAX = 0x1a
APPCOMMAND_MIC_MIN = 0x19
ERROR_THRESHOLD = 5

class VirtualWebcam():
    
    def __init__(self,  errImgPath=None, notPresent=False, isSleeping=False, controlMic=False, faceRecognition=False):
        self.notPresent = notPresent
        self.isSleeping = isSleeping
        self.controlMic = controlMic
        self.errImg = (None, cv.imread(errImgPath))[errImgPath is not None]
        self.blockFrame = None
        self.notPresentCounter = 0
        self.NotUser = False
        
        # Import all the cascades
        self.face_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_frontalface_default.xml')
        self.open_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_eye.xml')
        self.right_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_righteye_2splits.xml')
        self.left_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_lefteye_2splits.xml')
        if (faceRecognition):
            print("NOT NONE")
            self.face_recognizer = cv.face.LBPHFaceRecognizer_create()
            self.face_recognizer.read(str(pathlib.Path(__file__).resolve().parent)  + '/Data/JonathanPesce_Model.yml')
        else:
            self.face_recognizer = None
            
            
            
    def start(self):
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0) 
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"
        
        with pyvirtualcam.Camera(width=IMG_W, height=IMG_H, fps=26) as cam:
            counter = 0
            while True:
                frame = self.processFrame(video_feed, counter)
                counter = (counter + 1, 0)[counter == 30]
                
                # Send to virtual cam
                cam.send(frame)
                    
                # Wait until it's time for the next frame
                cam.sleep_until_next_frame()
               
                
        cv.waitKey(0)
        video_feed.release()

       

        
    def processFrame(self, video_feed, counter, isPython=False):
        # Read the frame from the webcam
        isTrue, frame = video_feed.read()
        
        if (counter % 5 == 0):
            if (self.updateShouldShowCame(frame, counter % 15 == 0 and self.face_recognizer is not None) == False):
                frame = self.getBlockFrame(frame, self.notPresent)
            elif (self.blockFrame is not None):
                self.blockFrame = None
                
                if (self.controlMic):
                    turnOnMic()
        elif (self.blockFrame is not None):
            frame = self.blockFrame
        
        # If we are pushing to OBS convert to RGBA
        if (isPython == False):
            frame = convert2RGBA(frame)
        
        
        return frame
    
    
    
    def updateShouldShowCame(self, frame, checkFace):
        if (self.notPresent == False and self.isSleeping == False and checkFace == False and self.NotUser == False):
            return True
        
        # Convert the frame to grayscale
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # Grab all the faces found
        face_rects = self.face_cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=10)
        
        # Check based on restrictions passed in if conditions to turn off are met
        shouldTurnOff = False
        
        if (checkFace):
            for (x,y,w,h) in face_rects:
                faces_roi = frame_gray[y:y+h, x:x+w]
                label, confidence = self.face_recognizer.predict(faces_roi)
                
                if (label != 1):
                    print("NOT USER")
                    self.NotUser = False
                    return False
                else:
                    print("Is User")
                    self.NotUser = True
        else:
            if (self.NotUser == False):
                return False
        
        # If user is not present turn off the webcam
        if (self.notPresent and len(face_rects) < 1):
            shouldTurnOff = True
            
            
        if (shouldTurnOff == False and self.isSleeping and self.detectSleeping(face_rects, frame_gray)):
            shouldTurnOff = True
             
        self.notPresentCounter = (0, self.notPresentCounter + 1)[shouldTurnOff]
        return self.notPresentCounter < ERROR_THRESHOLD
    
    
    
    
    
    def getBlockFrame(self, frame, notPresent):
        if (self.blockFrame is not None):
            return self.blockFrame
            
        if (self.errImg is not None):
            self.blockFrame = self.errImg
        else:
            self.blockFrame = cv.blur(frame, (131,131))
            
            if (notPresent):
                self.blockFrame = cv.putText(self.blockFrame, 'LEFT THE SCREEN', (20, IMG_H//2), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv.LINE_AA)
        
        # Turn off the mic 
        if (self.controlMic):
            turnOffMic()
        
        return self.blockFrame
    
    
    
    
    
    def detectSleeping(self, faces_rect, frame_gray):
        # Check if there was a face that was detected
        if (len(faces_rect) < 0):            
            return False
            
        for (x,y,w,h) in faces_rect:   
            # Get the ROI of the image
            roi = frame_gray[y:y+h,x:x+w]
            
            oeyes = self.open_eyes_cascade.detectMultiScale(roi,1.3,30)
            reyes = self.right_eyes_cascade.detectMultiScale(roi,1.3,20)
            leyes = self.left_eyes_cascade.detectMultiScale(roi,1.3,20)
            
            if (len(leyes)!=0 or len(reyes) !=0) and len(oeyes) == 0:
                return True
        
        return False
            
    
    
    def startPython(self):
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0)
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"
        
        counter = 0
        while True:
            frame = self.processFrame(video_feed, counter, isPython=True)
            
            counter = (counter + 1, 0)[counter == 30]
            
            cv.imshow('Title', frame) 
            cv.waitKey(1)
        
        cv.waitKey(0)
        video_feed.release()
  

def toggleMic(val):
    win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, val * 0x10000)
  
def turnOffMic():
    thread = Thread(target=toggleMic, args=([APPCOMMAND_MIC_MIN]))
    thread.start()
    
def turnOnMic():
    thread = Thread(target=toggleMic, args=([APPCOMMAND_MIC_MAX]))
    thread.start()

def convert2RGBA(frame):
    # convert to RGBA
    out_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out_frame_rgba = np.zeros((IMG_H, IMG_W, 4), np.uint8)
    out_frame_rgba[:, :, :3] = out_frame
    out_frame_rgba[:, :, 3] = 255
    cv.flip(out_frame_rgba, -1)
    return out_frame_rgba

t = VirtualWebcam(notPresent=False, isSleeping=False, errImgPath='ErrorImage.png', controlMic=False, faceRecognition=True)
#t.startPython()
t.start()