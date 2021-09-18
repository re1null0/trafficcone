#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:07:49 2021

@author: shyryn
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

filepath = 'traffic-cones-5.ppm'
with open(filepath, 'rb') as fobj:
    raw_bytes = fobj.read()

arr = str(raw_bytes[:14])
if ('P6' in str(raw_bytes)):
    height = int(arr.split()[1])
    width = int(arr.split()[2])
    new_bytes = raw_bytes[(len(raw_bytes)-width*height*3):]
    raw = ' '.join(map(lambda x: '{:08}'.format(x), new_bytes)).split()
    
    raw_to_int = []
    for i in range(0, len(raw)):
        raw_to_int.append(int(str(raw[i]), 10))
        
    raw_to_int = np.asarray(raw_to_int, dtype='uint8')
    new_rgb = raw_to_int.reshape(width, height, 3)
    plt.imshow(new_rgb)
    ORANGE_MIN = np.array([0, 40, 66])
    ORANGE_MAX = np.array([16, 217, 255])
    if(filepath=='traffic-cones-6.ppm'):
        hls_img = cv2.cvtColor(new_rgb,cv2.COLOR_BGR2HLS)
    else:
        hls_img = cv2.cvtColor(new_rgb,cv2.COLOR_RGB2HLS)
    frame_threshed = cv2.inRange(hls_img, ORANGE_MIN, ORANGE_MAX)
    #plt.imshow(frame_threshed)
    kernel = np.ones((3, 3))
    img_thresh_opened = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, kernel)
    
    img_thresh_blurred = cv2.medianBlur(img_thresh_opened, 5)
    #plt.imshow(img_thresh_blurred)
    img_edges = cv2.Canny(img_thresh_blurred, 100, 160)
    contours, hierarchy = cv2.findContours(np.array(img_edges), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros_like(img_edges)
    cv2.drawContours(img_contours, contours, -1, (255,255,255), 2)
    plt.imshow(img_contours)
    #cv2.imwrite('output5.png', img_contours)
else: 
    with open(filepath, 'r', encoding='utf-8') as ppm:
        data = ppm.read()
        encoding, height, width, *values = data.split()

    rgb = [list(values[i:i+3]) for i in range(1, len(values), 3)]
    npa = np.asarray(rgb, dtype='uint8')
    new_rgb = npa.reshape((int(width), int(height), 3)) 
    #plt.imshow(npnew)
    image = new_rgb
    
    ORANGE_MIN = np.array([0, 40, 66])
    ORANGE_MAX = np.array([16, 217, 255])
    
    hls_img = cv2.cvtColor(image,cv2.COLOR_RGB2HLS)
    
    frame_threshed = cv2.inRange(hls_img, ORANGE_MIN, ORANGE_MAX)
    #plt.imshow(frame_threshed)
    kernel = np.ones((3, 3))
    img_thresh_opened = cv2.morphologyEx(frame_threshed, cv2.MORPH_OPEN, kernel)
    
    img_thresh_blurred = cv2.medianBlur(img_thresh_opened, 5)
    #plt.imshow(img_thresh_blurred)
    img_edges = cv2.Canny(img_thresh_blurred, 100, 160)
    contours, hierarchy = cv2.findContours(np.array(img_edges), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros_like(img_edges)
    cv2.drawContours(img_contours, contours, -1, (255,255,255), 2)
    plt.imshow(img_contours)