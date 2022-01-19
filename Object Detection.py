from typing import Counter
import cv2
import torch
import numpy as np
import time
import os
from tracker import *
#from CDTPMySQL import connectToMySQL, queryToMySQL
from datetime import datetime
from trackerLib import CentroidTracker
import serial
import time

arduino_serial = serial.Serial("com4",115200)

# Load the yolov5 model.. Model will get downloaded when executed
model = torch.hub.load("ultralytics/yolov5", "yolov5l")

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

cap = cv2.VideoCapture(1)

tracker1 = EuclideanDistTracker(1)
ct = CentroidTracker()
(H, W) = (None, None)
frameCounter = 0


#dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')

duranCounter = 0

while True:

    rects1 = []
    Class1 = []

    #os.system("cls")
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    results = model(frame)
    # print(results.pandas().xyxy[0])
    # print(type(results.pandas().xyxy[0]))
    new_frame = np.squeeze(results.render())

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    

    df = results.pandas().xyxy[0]
    dummy = df.values.tolist()

    for i in range(len(dummy)):
        rects1.append([int(dummy[i][0]), int(dummy[i][1]), int(dummy[i][2]) - int(dummy[i][0]), int(dummy[i][3]) - int(dummy[i][1]),int(dummy[i][5])])
        Class1.append([int(dummy[i][5])])

    # lengthh = len(dummy)
    # xLeftBottom = df["xmin"]
    # yLeftBottom = df["ymin"]
    # xRightTop = df["xmax"]
    # yRightTop = df["ymax"]
    # Class = df["class"]



    

    # rects1.append([int(xLeftBottom), int(yLeftBottom), int(xRightTop) - int(xLeftBottom), int(yRightTop) - int(yLeftBottom)])

    boxes_ids, numStoppedCar = tracker1.update(rects1, Class1)

    # this code is executed every 10 frames
    if frameCounter == 10:
        anomaly1 = tracker1.detectAnimal()
        anomaly2 = tracker1.detectStoppedCars()
        anomaly3 = tracker1.detectReversedCars('horizontal')
        anomaly4 = tracker1.detectKamyon()
        datasent = str(anomaly1)+str(anomaly2)+str(anomaly3)+str(anomaly4)
        
        if datasent != '0000':
            for i in range(10):
                arduino_serial.write(bytes(datasent,encoding='utf-8'))
            #duranCounter = 0
        #else:
            #duranCounter += 1
            #if duranCounter == 10:
             #   arduino_serial.write(bytes(datasent,encoding='utf-8'))
        frameCounter = 0
    #cv2.putText(new_frame,boxes_ids[4],)

    #if (numStoppedCar > 0):
        #print("DURAN ARABA")
    #else:
        #print("ARABA HAREKET HALİNDE")
    
    # down_width = 600
    # down_height = 600
    # down_points = (down_width, down_height)
    # new_frame = cv2.resize(new_frame, down_points, interpolation= cv2.INTER_LINEAR)
    
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX

    for x,y,w,h,id in boxes_ids:
        cv2.putText(new_frame,str(id),(x,y+h),font,1,(255, 0, 0),1,cv2.LINE_AA)
    # time when we finish processing for this frame
    new_frame_time = time.time()
    
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    
    cv2.putText(new_frame, fps, (7, 70), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    
    cv2.imshow('Yolo', new_frame)

    frameCounter +=1
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1)
        
cap.release()
cv2.destroyAllWindows()
