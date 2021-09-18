#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:23:26 2021

@author: shyryn
"""
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from taskA_part1 import image

def nothing(x):
    pass


# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('LMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('LMax', 'image', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('LMax', 'image', 255)

# Initialize HSV min/max values
hMin = sMin = lMin = hMax = sMax = lMax = 0
phMin = psMin = plMin = phMax = psMax = plMax = 0

while(1):
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    lMin = cv2.getTrackbarPos('LMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    lMax = cv2.getTrackbarPos('LMax', 'image')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, lMin, sMin])
    upper = np.array([hMax, lMax, sMax])

    # Convert to HSV format and color threshold
    hsl = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    mask = cv2.inRange(hsl, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (plMin != lMin) | (phMax != hMax) | (psMax != sMax) | (plMax != lMax) ):
        print("(hMin = %d , sMin = %d, lMin = %d), (hMax = %d , sMax = %d, lMax = %d)" % (hMin , sMin , lMin, hMax, sMax , lMax))
        phMin = hMin
        psMin = sMin
        plMin = lMin
        phMax = hMax
        psMax = sMax
        plMax = lMax

    # Display result image
    cv2.imshow('image', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()