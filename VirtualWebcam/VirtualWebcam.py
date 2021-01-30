# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:18:23 2021

@author: jonat
"""

import cv2 as cv

class VirtualWebcam():
    
    def __init__(self, errImgPath=None):
        self.face_cascade = cv.CascadeClassifier('haar_face.xml')
        self.terminate = True
        
        if (errImgPath is not None):
            self.errImg = cv.imread(errImgPath)
    
    def start():
        self.terminate = False
        
        try: 
            while True:
                print("TTT")
        finally:
            cv.release()
            
    
    
    
    def terminate():
        print('Terminate')        
            
