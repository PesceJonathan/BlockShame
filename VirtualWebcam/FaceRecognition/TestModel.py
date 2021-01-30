# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 02:48:31 2021

@author: jonat
"""
import cv2 as cv
from FormatImage import formatImage

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('../Data/JonathanPesce_Model.yml')

# Import the face cascade
face_cascade = cv.CascadeClassifier('../Haarcascades/haarcascade_frontalface_default.xml')

# Use OpenCV to grab the webcam video feed
video_feed = cv.VideoCapture(0)

while True:
    # Read the frame
    isTrue, frame = video_feed.read()
    img = formatImage(frame, face_cascade)
    
    if (len(img) > 0):    
        label, confidence = face_recognizer.predict(img[0])
        frame = cv.putText(frame, f"{label} with {confidence}", (20, 400), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv.LINE_AA)
    
    cv.imshow("Frame", frame)    
    cv.waitKey(1)


cv.waitKey(0)
video_feed.release()
cv.destroyAllWindows()