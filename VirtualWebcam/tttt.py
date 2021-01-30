# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:18:23 2021

@author: jonat
"""

import cv2 as cv
# import pyvirtualcam
# import numpy as np

# Constants
IMG_W = 640
IMG_H = 480
ERROR_THRESHOLD = 12


class VirtualWebcam():
    
    def __init__(self, errImgPath=None):
        self.face_cascade = cv.CascadeClassifier('haar_face.xml')
        self.terminate = True
        self.noFaceDetected = 0
        self.errImg = (None, cv.imread(errImgPath))[errImgPath is not None]

    
    def start(self):
        self.terminate = False
        self.noFaceDetected = 0
        

        # Use OpenCV to grab the webcam video feedf
        video_feed = cv.VideoCapture(0)
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"
        
        
        while True:
            isTrue, frame = video_feed.read()
            cv.imshow('Title', frame) 
            
            if cv.waitKey(1) == 27:
                break
            

        cv.waitKey(0)
        video_feed.release()
        cv.destroyAllWindows()
    

    
    
t = VirtualWebcam()
t.start()
         