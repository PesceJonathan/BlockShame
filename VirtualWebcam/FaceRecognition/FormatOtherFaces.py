# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 01:36:34 2021

@author: jonat
"""
import cv2 as cv
import numpy as np
import os
from FormatImage import formatImage

IMG_W = 640
IMG_H = 480

face_cascade = cv.CascadeClassifier('../Haarcascades/haarcascade_frontalface_default.xml')

path = '../Data/OtherFaces'
features = []

length = len(os.listdir(path))
counter = 0

# Loop through all the images
for img in os.listdir(path):
    counter += 1
    print(f"{counter}/{length}")
    
    img_path = os.path.join(path, img)
    img = cv.imread(img_path)
    features.extend(formatImage(img, face_cascade))
    
    if (counter == 200):
        break
    
    
# Save the array as a file
np.save('../Data/OtherFeatures.npy', np.array(features))