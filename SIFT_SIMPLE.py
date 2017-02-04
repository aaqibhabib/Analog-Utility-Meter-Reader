import cv2
from pymongo import MongoClient
import time
import datetime
import urllib 
import numpy as np

timestamp=time.time()
#        cv2.imshow('RAW',img)
src_img =  cv2.imread('iphone.jpg',0)          # queryImage
img =  cv2.imread('meter.jpg',0)   
# Initiate STAR detector
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints with ORB
kp1, des1 = sift.detectAndCompute(src_img,None)
kp2, des2 = sift.detectAndCompute(img,None)
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
        # cv2.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(src_img,kp1,img,kp2,good[:10],None,flags=2)
cv2.imshow('keypoints',img3)
cv2.waitKey(0)
# Find circles of known radius and draw them
gray = (cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
#        equalized_gray = cv2.equalizeHist(gray)

# Find most prominent lines and draw them
edges = cv2.Canny(gray,25,100,apertureSize = 3)
lines = cv2.HoughLines(edges,1,np.pi/200,180)
avg_theta = 0
for rho,theta in lines[0]:
    avg_theta += theta
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img,(x1,y1),(x2,y2),(230,255,2),1)

# Fix image rotation
#print(360*avg_theta/lines[0].size/2-90)
#M = cv2.getRotationMatrix2D((640/2,480/2),360*avg_theta/lines[0].size/2-91.87,1)
#img = cv2.warpAffine(img,M,(640,480))

#cv2.imshow('Equalized',gray)
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,10,param1=25,param2=25,minRadius=30,maxRadius=45)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
#            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
#            cv2.circle(img,(i[0],i[1]),2,(0,0,255),1)
    # draw the brightest spot in this circle
    r = 10
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray[i[1]-r:i[1]+r, i[0]-r:i[0]+r])
    cv2.circle(img, (maxLoc[0]+i[0]-r,maxLoc[1]+i[1]-r), 2, (0, 255, 0), 2)
    cv2.circle(img, (maxLoc[0]+i[0]-r,maxLoc[1]+i[1]-r), i[2], (0,0,255),2)
    # take the avg_point between brightest_spot & center_of_circle as mathematical center 

M = cv2.getRotationMatrix2D((640/2,480/2),360*avg_theta/lines[0].size/2-91.87,1)                                                                          
img = cv2.warpAffine(img,M,(640,480))  
cv2.imshow('gray,edge,hough,rotate',img)
cv2.waitKey(0)
print(time.time()-timestamp)
timestamp=time.time() 
