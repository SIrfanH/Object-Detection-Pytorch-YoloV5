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
from CDTPMySQL import *

dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')

anomaly1 = 0
anomaly2 = 0
anomaly3 = 0
anomaly4 = 0

anomaly1_2 = 0
anomaly2_2 = 0
anomaly3_2 = 0
anomaly4_2 = 0


#arduino_serial = serial.Serial("com11",115200)    COMMENTI KALDIR
#arduino_serial2 = serial.Serial("com3",115200)    COMMENTI KALDIR

# Load the yolov5 model.. Model will get downloaded when executed
model = torch.hub.load("ultralytics/yolov5", "yolov5l")

# used to record the time when we processed last frame
prev_frame_time = 0
prev_frame_time2 = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0
new_frame_time2 = 0

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

tracker1 = EuclideanDistTracker(1)
tracker2 = EuclideanDistTracker(2)
ct = CentroidTracker()
(H, W) = (None, None)
frameCounter = 0
frameCounter2 = 0


dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')

duranCounter = 0
duranCounter2 = 0

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
                pass
                #print("VERİ GÖNDER")
                #arduino_serial.write(bytes(datasent,encoding='utf-8'))
            print("VERİ GÖNDER")
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
    
    #cv2.imshow('Yolo', new_frame)

    frameCounter +=1




    rects2 = []
    Class2 = []

    #os.system("cls")
    ret2, frame2 = cap2.read()
    
    if not ret:
        break
    
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    results2 = model(frame2)
    # print(results.pandas().xyxy[0])
    # print(type(results.pandas().xyxy[0]))
    new_frame2 = np.squeeze(results2.render())

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    

    df2 = results2.pandas().xyxy[0]
    dummy = df2.values.tolist()

    for i in range(len(dummy)):
        rects2.append([int(dummy[i][0]), int(dummy[i][1]), int(dummy[i][2]) - int(dummy[i][0]), int(dummy[i][3]) - int(dummy[i][1]),int(dummy[i][5])])
        Class2.append([int(dummy[i][5])])

    # lengthh = len(dummy)
    # xLeftBottom = df["xmin"]
    # yLeftBottom = df["ymin"]
    # xRightTop = df["xmax"]
    # yRightTop = df["ymax"]
    # Class = df["class"]



    

    # rects1.append([int(xLeftBottom), int(yLeftBottom), int(xRightTop) - int(xLeftBottom), int(yRightTop) - int(yLeftBottom)])

    boxes_ids2, numStoppedCar2 = tracker2.update(rects2, Class2)

    # this code is executed every 10 frames
    if frameCounter2 == 10:
        anomaly1_2 = tracker2.detectAnimal()
        anomaly2_2 = tracker2.detectStoppedCars()
        anomaly3_2 = tracker2.detectReversedCars('horizontal')
        anomaly4_2 = tracker2.detectKamyon()
        datasent_2 = str(anomaly1_2)+str(anomaly2_2)+str(anomaly3_2)+str(anomaly4_2)
        
        if datasent != '0000':            
            for i in range(10):
                pass
                #print("VERİ GÖNDER")
                #arduino_serial2.write(bytes(datasent_2,encoding='utf-8'))
            print("VERİ")
                
            #duranCounter = 0
        #else:
            #duranCounter += 1
            #if duranCounter == 10:
             #   arduino_serial.write(bytes(datasent,encoding='utf-8'))
        frameCounter2 = 0
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

    for x,y,w,h,id in boxes_ids2:
        cv2.putText(new_frame2,str(id),(x,y+h),font,1,(255, 0, 0),1,cv2.LINE_AA)
    # time when we finish processing for this frame
    new_frame_time2 = time.time()
    
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1/(new_frame_time2-prev_frame_time2)
    prev_frame_time = new_frame_time2
    fps2 = str(int(fps))
    
    cv2.putText(new_frame2, fps2, (7, 70), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    
    #cv2.imshow('Yolo', new_frame)

    frameCounter2 +=1

    cv2.imshow('Merkezi Kontrol Birimi', np.concatenate((new_frame, new_frame2), axis=1))  
    query1 = f'UPDATE cdtp SET anomaly_2=("{anomaly2}"), anomaly_1=("{anomaly1}"), anomaly_3=("{anomaly3}"), anomaly_4=("{anomaly4}"), timestamp=("{current_time}") WHERE cam_id=({1});'
    query2 = f'UPDATE cdtp SET anomaly_2=("{anomaly2_2}"), anomaly_1=("{anomaly1_2}"), anomaly_3=("{anomaly3_2}"), anomaly_4=("{anomaly4_2}"), timestamp=("{current_time}") WHERE cam_id=({2});'

    #query2 = f'UPDATE cdtp SET anomaly_1=' + str(anomaly1_2), +  ', anomaly_2=' + str(anomaly2_2) + ', anomaly_3=' + str(anomaly3_2)+ ', anomaly_4=' +str(anomaly4_2) + ', timestamp=("{current_time}") WHERE cam_id=({2});'
    #query1 = f'UPDATE cdtp SET anomaly_1=' + str(anomaly1), +  ', anomaly_2=' + str(anomaly2) + ', anomaly_3=' + str(anomaly3)+ ', anomaly_4=' +str(anomaly4) + ', timestamp=("{current_time}") WHERE cam_id=({1});'

    queryToMySQL(dataBaseCursor, dataBaseConn, query2)
    queryToMySQL(dataBaseCursor, dataBaseConn, query1)
    

    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('p'):
        cv2.waitKey(-1)
        
cap.release()
cap2.release()
cv2.destroyAllWindows()