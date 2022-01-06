import cv2
import torch
import numpy as np
import time

# Load the yolov5 model.. Model will get downloaded when executed
model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    results = model(frame)
    new_frame = np.squeeze(results.render())
    
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
    
    cv2.putText(new_frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    
    cv2.imshow('Yolo', new_frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()