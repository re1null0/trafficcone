#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:23:09 2021

@author: shyryn
"""
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
file_path = 'traffic-cones-1.ppm'

with open(file_path, 'r', encoding='utf-8') as ppm:
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
#cv2.imwrite('output4.png', img_contours)

'''
BETTER WAY


approx_contours = []

for c in contours:
    approx = cv2.approxPolyDP(c, 10, closed = True)
    approx_contours.append(approx)

img_approx_contours = np.zeros_like(img_edges)
cv2.drawContours(img_approx_contours, approx_contours, -1, (255,255,255), 1)
all_convex_hulls = []
for ac in approx_contours:
    all_convex_hulls.append(cv2.convexHull(ac))
img_all_convex_hulls = np.zeros_like(img_edges)
cv2.drawContours(img_all_convex_hulls, all_convex_hulls, -1, (255,255,255), 2)
convex_hulls_3to10 = []
for ch in all_convex_hulls:
    if 3 <= len(ch) <= 10:
        convex_hulls_3to10.append(cv2.convexHull(ch))

img_convex_hulls_3to10 = np.zeros_like(img_edges)
cv2.drawContours(img_convex_hulls_3to10, convex_hulls_3to10, -1, (255,255,255), 2)
plt.imshow(img_convex_hulls_3to10)
plt.show()
'''

