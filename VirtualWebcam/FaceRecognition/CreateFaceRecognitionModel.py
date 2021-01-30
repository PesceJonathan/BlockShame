# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 00:58:47 2021

@author: jonat
"""
import cv2 as cv
import numpy as np
from FormatImage import formatImage

MODAL_FILE_NAME = "../Data/{}_Model.yml"

class CreateFaceRecognitionModel():
    
    def __init__(self, modelName):
        self.modelName = modelName
        self.dataSet = []
        
    def createDataset(self):
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0)
        
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"
        
        while len(self.dataSet) < 100:
            # Read the frame
            isTrue, frame = video_feed.read()
            self.dataSet.append(frame)
            cv.waitKey(100)
            print(str(len(self.dataSet)))
        
        
        cv.waitKey(0)
        video_feed.release()
        cv.destroyAllWindows()
    
    
    
    def createModel(self):
        # Create our face_cascade
        face_cascade = cv.CascadeClassifier('../Haarcascades/haarcascade_frontalface_default.xml')
        
        # Get our features and labels array
        features = np.load('../Data/OtherFeatures.npy', allow_pickle=True)
        
        newFeatures = []
        
        # Append user dataset to features
        for img in self.dataSet:
            newFeatures.extend(formatImage(img, face_cascade))
        
        
        # Set labels to be a numpy 
        labels = [0]*len(features)
        labels.extend([1]*len(newFeatures))
        labels = np.array(labels)
        
        newFeatures = np.array(newFeatures, dtype='object')
        features = np.append(features, newFeatures)
        features = np.array(features, dtype='object')
        
        
        # Create the face recognizer
        face_recognizer = cv.face.LBPHFaceRecognizer_create()
        face_recognizer.train(features, labels)
        face_recognizer.save(MODAL_FILE_NAME.format(self.modelName))
        
        
recognition = CreateFaceRecognitionModel('JonathanPesce')
recognition.createDataset()
recognition.createModel()