# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 12:45:18 2021

@author: jonat
"""
# import cv2 as cv
from YOLO import YOLO

yolo = YOLO("../HandDetection/cross-hands-tiny-prn.cfg", "../HandDetection/cross-hands-tiny-prn.weights", "hand")

yolo.size = int(416)
yolo.confidence = float(0.2)