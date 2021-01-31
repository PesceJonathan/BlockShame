# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 02:48:31 2021

@author: jonat
"""
import cv2 as cv
from FormatImage import formatImage
import pandas as pd

# Import the face cascade
face_cascade = cv.CascadeClassifier('../Haarcascades/haarcascade_frontalface_default.xml')
face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('../Data/JonathanPesce_Model.yml')

# # Use OpenCV to grab the webcam video feed
# video_feed = cv.VideoCapture(0)

frames = []

data = pd.read_csv('VideoForTesting.csv')
data['Frames'].apply(lambda frame: frames.append(frame))



def run(ttt):
    for frame in ttt:
        frame = frame[0]
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces_rect = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=20)
        
        height = 460
        
        for (x,y,w,h) in faces_rect:
            faces_roi = frame_gray[y:y+h, x:x+w]
            label, confidence = face_recognizer.predict(faces_roi)
           
            person = ("Jonathan", "Dad")[label == 0]
           
            frame = cv.putText(frame, f"{person} with confidence {confidence}", (20, 460), cv.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv.LINE_AA)
            height = height - 20
           
        cv.imshow("Frame", frame)    
        frames.append(frame)
        cv.waitKey(1)
    
    
    cv.waitKey(0)
    cv.destroyAllWindows()




# img = formatImage(frame, face_cascade)

# if (len(img) > 0):    
#     label, confidence = face_recognizer.predict(img[0])
#     frame = cv.putText(frame, f"{label} with {confidence}", (20, 400), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv.LINE_AA)
