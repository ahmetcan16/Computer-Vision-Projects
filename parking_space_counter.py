import cv2
import pickle
import numpy as np

def checkParkSpace(imgg):
    spaceCounter = 0
    
    for pos in posList:
        x, y = pos
        
        img_crop = imgg[y: y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        
        # print("count: ", count)
        
        if count < 150:
            color = (0, 255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)
    
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2) 
        cv2.putText(img, str(count), (x, y + height - 2), cv2.FONT_HERSHEY_PLAIN, 1,color,1)
    
    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15,24), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,255),4)

width = 27
height = 15

cap = cv2.VideoCapture("video.mp4")

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

while True:
    success, img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)
    
    checkParkSpace(imgDilate)
    
    cv2.imshow("img", img)
    # cv2.imshow("img_gray", imgGray)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThreshold", imgThreshold)
    # cv2.imshow("imgMedian", imgMedian)
    # cv2.imshow("imgDilate", imgDilate)
    cv2.waitKey(200)
    
    
    
    
    
    