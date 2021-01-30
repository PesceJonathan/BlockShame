# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:18:23 2021

@author: jonat
"""

import cv2 as cv
import pyvirtualcam
import numpy as np

# Constants
IMG_W = 640
IMG_H = 480
ERROR_THRESHOLD = 12
BLUR_TEXT = 'Personal Stuff Happening'


class VirtualWebcam():
    
    def __init__(self, errImgPath=None):
        self.face_cascade = cv.CascadeClassifier('haar_face.xml')
        self.terminate = True
        self.noFaceDetected = 0
        self.errImg = (None, cv.imread(errImgPath))[errImgPath is not None]
        self.blurredImg = None
    
    def start(self):
        self.terminate = False
        self.noFaceDetected = 0
        
        # Use OpenCV to grab the webcam video feedf
        video_feed = cv.VideoCapture(0)
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"
        
        while True:
            frame = self.processFrame(video_feed)
            cv.imshow('Title', frame) 
                
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
        faces_rect = self.face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=10)
        
        # Check if no faces were detected, if so then increase no face detected counter
        self.noFaceDetected = (0, self.noFaceDetected + 1)[len(faces_rect) < 1]
        
        # Check if face is not detected, if so send blocking frame
        if (self.noFaceDetected > ERROR_THRESHOLD):
            frame = self.getBlockFrame(frame)
        else:
            self.blurredImg = None
        
        # # convert to RGBA
        # out_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # out_frame_rgba = np.zeros((IMG_H, IMG_W, 4), np.uint8)
        # out_frame_rgba[:, :, :3] = out_frame
        # out_frame_rgba[:, :, 3] = 255
            
        return frame
        
        
        
    def getBlockFrame(self, frame):
        if (self.errImg is not None):
            return self.errImg
        
        if (self.blurredImg is None):
            # blur the Image
            self.blurredImg = cv.blur(frame, (131,131))
            
            # Add text to the image
            self.blurredImg = cv.putText(self.blurredImg, BLUR_TEXT, (20, IMG_H//2), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv.LINE_AA)

        return self.blurredImg
    
    
    
# t = VirtualWebcam(errImgPath='ErrorImage.png')
t = VirtualWebcam()
t.start()