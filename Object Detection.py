import cv2
import torch
import numpy as np
import time
import os
from tracker import *
from CDTPMySQL import connectToMySQL, queryToMySQL
from datetime import datetime
from trackerLib import CentroidTracker

# Load the yolov5 model.. Model will get downloaded when executed
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# used to record the time when we processed last frame
prev_frame_time = 0
prev_frame_time2 = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0
new_frame_time2 = 0

cap = cv2.VideoCapture("Traffic Animation #01.mp4")
cap2 = cv2.VideoCapture("Traffic Animation - After Effect.mp4")

tracker1 = EuclideanDistTracker(1)
tracker2 = EuclideanDistTracker(2)
ct = CentroidTracker()
(H, W) = (None, None)

dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')


while True:

    rects1 = []
    Class1 = []

    rects2 = []
    Class2 = []

    #os.system("cls")
    ret, frame = cap.read()

    if not ret:
        break

    scale_percent = 40 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    
    
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
        rects1.append([int(dummy[i][0]), int(dummy[i][1]), int(dummy[i][2]) - int(dummy[i][0]), int(dummy[i][3]) - int(dummy[i][0])])
        Class1.append([int(dummy[i][5])])

    # lengthh = len(dummy)
    # xLeftBottom = df["xmin"]
    # yLeftBottom = df["ymin"]
    # xRightTop = df["xmax"]
    # yRightTop = df["ymax"]
    # Class = df["class"]

    

    # rects1.append([int(xLeftBottom), int(yLeftBottom), int(xRightTop) - int(xLeftBottom), int(yRightTop) - int(yLeftBottom)])

    boxes_ids, numStoppedCar = tracker1.update(rects1, Class1)

    if (numStoppedCar > 0):
        print("DURAN ARABA")
    else:
        print("ARABA HAREKET HALİNDE")
    
    # down_width = 600
    # down_height = 600
    # down_points = (down_width, down_height)
    # new_frame = cv2.resize(new_frame, down_points, interpolation= cv2.INTER_LINEAR)
    
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()
    
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    
    cv2.putText(new_frame, fps, (7, 25), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(new_frame, current_time, (7, 55), font, 1, (100, 255, 0), 1, cv2.LINE_AA)

    ret2, frame2 = cap2.read()
    
    if not ret2:
        break

    scale_percent = 40 # percent of original size
    width = int(frame2.shape[1] * scale_percent / 100)
    height = int(frame2.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    frame2 = cv2.resize(frame2, dim, interpolation = cv2.INTER_AREA)

    
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    results2 = model(frame2)
    # print(results.pandas().xyxy[0])
    # print(type(results.pandas().xyxy[0]))
    new_frame2 = np.squeeze(results2.render())

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    

    df = results2.pandas().xyxy[0]
    dummy = df.values.tolist()

    for i in range(len(dummy)):
        rects2.append([int(dummy[i][0]), int(dummy[i][1]), int(dummy[i][2]) - int(dummy[i][0]), int(dummy[i][3]) - int(dummy[i][0])])
        Class2.append([int(dummy[i][5])])

    # lengthh = len(dummy)
    # xLeftBottom = df["xmin"]
    # yLeftBottom = df["ymin"]
    # xRightTop = df["xmax"]
    # yRightTop = df["ymax"]
    # Class = df["class"]

    

    # rects1.append([int(xLeftBottom), int(yLeftBottom), int(xRightTop) - int(xLeftBottom), int(yRightTop) - int(yLeftBottom)])

    boxes_ids2, numStoppedCar2 = tracker2.update(rects2, Class2)

    if (numStoppedCar2 > 0):
        print("DURAN ARABA")
    else:
        print("ARABA HAREKET HALİNDE")
    
    # down_width = 600
    # down_height = 600
    # down_points = (down_width, down_height)
    # new_frame = cv2.resize(new_frame, down_points, interpolation= cv2.INTER_LINEAR)
    
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time2 = time.time()
    
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps2 = 1/(new_frame_time2-prev_frame_time2)
    prev_frame_time2 = new_frame_time
    fps2 = str(int(fps))
    
    cv2.putText(new_frame2, fps2, (7, 25), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(new_frame2, current_time, (7, 55), font, 1, (100, 255, 0), 1, cv2.LINE_AA)

    
    cv2.imshow('Merkezi Kontrol Birimi', np.concatenate((new_frame, new_frame2), axis=1))
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cap2.release()
cv2.destroyAllWindows()