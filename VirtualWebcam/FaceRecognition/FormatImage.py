# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 01:27:37 2021

@author: jonat
"""
import cv2 as cv

def formatImage(img, face_cascade):
    # Transform the image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Grab all of the faces detected within the image
    faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    
    # Create our empty features array
    features = []
    
    for (x,y,w,h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+w]
        features.append(faces_roi)
        
    return features