# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:18:23 2021

@author: jonat
"""

import cv2 as cv
import pyvirtualcam
import numpy as np
import pathlib
import os
# Constants
IMG_W = 640
IMG_H = 480
ERROR_THRESHOLD = 40
SLEEPING_THRESHOLD = 10
USER_THRESHOLD = 10
BLUR_TEXT = 'Personal Stuff Happening'
SLEEPING_TEXT = 'BLURED BECAUSE SLEEPING'

class VirtualWebcam():
    
    def __init__(self, errImgPath=None, checkSleep=False):
        self.face_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_frontalface_default.xml')
        self.open_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_eye.xml')
        self.right_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_righteye_2splits.xml')
        self.left_eyes_cascade = cv.CascadeClassifier(str(pathlib.Path(__file__).resolve().parent)  + './Haarcascades/haarcascade_lefteye_2splits.xml')
        # breakpoint()
        self.terminate = True
        self.noFaceDetected = 0
        self.isSleeping = False
        self.sleepCounter = 0
        self.isUser = False
        self.isUserCounter = 0
        self.errImg = (None, cv.imread(errImgPath))[errImgPath is not None]
        self.checkSleep = checkSleep == True
        self.blurredImg = None
        self.face_recognizer = cv.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read(str(pathlib.Path(__file__).resolve().parent)  + '/Data/JonathanPesce_Model.yml')
        self.message_queue = None
    
    def start(self):
        self.terminate = False
        self.noFaceDetected = 0
        
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0)
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"

        counter = 0

        with pyvirtualcam.Camera(width=IMG_W, height=IMG_H, fps=30) as cam:
            print("Running")
            while True:
                if counter == 30:
                    print(self.message_queue)
                    counter = 0

                counter += 1
                
                frame = self.processFrame(video_feed)
                # cv.imshow('Title', frame) 
                
                # Send to virtual cam
                cam.send(frame)
                    
                # Wait until it's time for the next frame
                cam.sleep_until_next_frame()
                    
                if cv.waitKey(1) == 27:
                    break
        
        
        
        cv.waitKey(0)
        video_feed.release()
        cv.destroyAllWindows()
     
            



    """
    Function will process the frame in order to decide what action are necessary to
    take
    
    Return Frame to send to webcam feed
    """
    def processFrame(self, video_feed):
        # Read the frame
        isTrue, frame = video_feed.read()
        
        # Convert the frame to grayscale
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # Get the faces that are detected in the frame
        faces_rect = self.face_cascade.detectMultiScale(frame_gray, scaleFactor=1.2, minNeighbors=10)
        
        # Check if the person detected is sleeping
        sleeping = self.checkSleep and self.checkForSleep(faces_rect, frame_gray)
        
        # Check if it is the current user
        currentUser = self.testIfUser(faces_rect, frame_gray)
        
        # Check if no faces were detected, if so then increase no face detected counter
        self.noFaceDetected = (0, self.noFaceDetected + 1)[len(faces_rect) < 1 or sleeping or currentUser]
        
        # Check if face is not detected, if so send blocking frame
        if (self.noFaceDetected > ERROR_THRESHOLD):
            frame = self.getBlockFrame(frame, sleeping, currentUser)
        else:
            self.blurredImg = None
        
        
        
        # Draw the rectangles for debugging purposes
        for (x,y,w,h) in faces_rect:
            cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=1)
        
            
        
        # convert to RGBA
        out_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        out_frame_rgba = np.zeros((IMG_H, IMG_W, 4), np.uint8)
        out_frame_rgba[:, :, :3] = out_frame
        out_frame_rgba[:, :, 3] = 255
        cv.flip(out_frame_rgba, -1)
        # out_frame_rgba = frame    
        
        
        return out_frame_rgba
        
    
    def checkForSleep(self, faces_rect, frame_gray):
        sleeping = self.detectSleeping(faces_rect, frame_gray)
    
        if (self.isSleeping and sleeping == False) or (self.isSleeping == False and sleeping): 
            self.sleepCounter += 1
        else:
            self.sleepCounter = 0
            
        if (self.sleepCounter > SLEEPING_THRESHOLD):
            self.isSleeping = not self.isSleeping
        
        return self.isSleeping
    
    
    
    def testIfUser(self, framge_gray, faces_rect):
        return False
        
        currentFrameUser = False
        
        for (x,y,w,h) in faces_rect:
            faces_roi = framge_gray[y:y+h, x:x+w]
            label, confidence = self.face_recognizer.predict(faces_roi)
            
            if (label == 1): 
                currentFrameUser = True
                break
        
        if (self.isUser and currentFrameUser == False) or (self.isUser == False and currentFrameUser == True):
            self.isUserCounter += 1
        else:
            self.isUserCounter = 0
            
            
        if (self.isUserCounter > USER_THRESHOLD):
            self.isUser = not self.isUser

        return self.isUser     

        
    
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
        
    
    
    def getBlockFrame(self, frame, sleeping, currentUser):
        if (self.errImg is not None):
            return self.errImg
        
        if (self.blurredImg is None):
            # blur the Image
            self.blurredImg = cv.blur(frame, (131,131))
            
            # Display different text if sleeping or not
            text = (BLUR_TEXT, SLEEPING_TEXT)[sleeping]
            
            # Display different currentUser text
            text = (text, "NOT JONATHAN")[currentUser]
            
            
            # Add text to the image
            self.blurredImg = cv.putText(self.blurredImg, text, (20, IMG_H//2), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv.LINE_AA)

        return self.blurredImg
    
    
if(__name__ == str('__main__')):    
    # t = VirtualWebcam(errImgPath='ErrorImage.png', checkSleep=True)
    t = VirtualWebcam(checkSleep=True)
    t.start()