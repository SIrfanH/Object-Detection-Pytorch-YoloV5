import math
import socket
from time import sleep
import os
from CDTPMySQL import connectToMySQL, queryToMySQL
from datetime import datetime


class EuclideanDistTracker:
    def __init__(self, id):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.cam_id = id
        # Define the connection credentials
        dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')
        self.cursor = dataBaseCursor
        self.conn = dataBaseConn     
           

    # 1 -> DURAN ARABA, 2 -> YOLDA İNSAN, 3 -> DENEME
    def update(self, objects_rect):

        numStoppedCar = 0
        
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])


                if dist < 25:

                    print("Aynı obje!!")

                    if dist < 15:

                        numStoppedCar += 1


                        
                    self.center_points[id] = (cx, cy)
                    #print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        if numStoppedCar > 0:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            print("DURAN ARABA:" + str(self.cam_id))
            query = f'UPDATE cdtp SET anomaly_1=("{1}"), timestamp=("{current_time}") WHERE cam_id=({self.cam_id});'
            queryToMySQL(self.cursor, self.conn, query)
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            print("DURAN ARABA YOK: " + str(self.cam_id))
            query = f'UPDATE cdtp SET anomaly_1=("{0}"), timestamp=("{current_time}") WHERE cam_id=({self.cam_id});'
            queryToMySQL(self.cursor, self.conn, query)            
        os.system("cls")
        numStoppedCar = 0

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



