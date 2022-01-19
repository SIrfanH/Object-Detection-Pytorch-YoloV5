import math
import socket
from time import sleep
import os
#from CDTPMySQL import connectToMySQL, queryToMySQL
from datetime import datetime
import numpy as np
import string


class EuclideanDistTracker:
    def __init__(self, id):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.cam_id = id
        # Define the connection credentials
        #dataBaseConn, dataBaseCursor = connectToMySQL('92.205.4.52', 'lvad', 'kaan', 'kaan1999')
        #self.cursor = dataBaseCursor
        #self.conn = dataBaseConn  

        # For storing much older position of the objects
        self.older_center_points = {}   
           

    # 1 -> DURAN ARABA, 2 -> YOLDA İNSAN, 3 -> DENEME
    def update(self, objects_rect, Class):

        numStoppedCar = 0
        name = Class

        numStoppedCar = 0
        
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        index = 0
        for rect in objects_rect:
            x, y, w, h, sinif = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])


                if dist < 25:

                    #print("Aynı obje!!")

                    # if dist < 15 and int(np.squeeze(name[index])) == 2:

                    #     numStoppedCar += 1
                    #     index += 1
                    # else:
                    #     index += 1

                
                        
                    self.center_points[id] = (cx, cy, sinif)
                    #print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy, sinif)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                
        """""
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
            """"" 
        #os.system("cls")
        

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids, numStoppedCar

    def detectReversedCars(self, orientaion):
        # Check if we have list of 5 frame old position
        deger = 0
        if len(self.older_center_points):
            for id, center in self.center_points.items():
                if orientaion == 'vertical':
                    if self.older_center_points.get(id):
                        #print(self.center_points_5frame.get(id))
                        centerX5F,centerY5F, sinif = self.older_center_points[id]
                        ydiff = center[1] - centerY5F
                        #print(ydiff)
                        if(ydiff<-5 and sinif == 2):
                            print("Ters Giden Araba " + str(id))
                            deger = 1

                else:
                    if self.older_center_points.get(id):
                        centerX5F,centerY5F, sinif = self.older_center_points[id]
                        xdiff = center[0] - centerX5F
                        if(xdiff<-5 and sinif == 2):
                            print("Ters Giden Araba "+ str(id))
                            deger = 1
            self.older_center_points = {}
            return deger
        else:
            self.older_center_points = self.center_points.copy()
            return deger

    def detectStoppedCars(self):
        if len(self.older_center_points):
            for id, center in self.center_points.items():
                 if self.older_center_points.get(id):
                    #print(self.center_points_5frame.get(id))
                    centerX5F,centerY5F, sinif = self.older_center_points[id]
                    #dist = math.hypot(center[0] - center, cy - pt[1])
                    xdiff = center[0] - centerX5F
                    #print(ydiff)
                    if(xdiff<5 and sinif == 2):
                        print("Duran Araba " + str(id))
                        return 1
        return 0

    def detectAnimal(self):
        for id, center in self.center_points.items():
            if center[2] in range(15,25):
                print("hayvan tespit edildi")
                return 1
        return 0
    def detectKamyon(self):
        for id, center in self.center_points.items():
            if center[2] in [7,5]:
                print("Yolda Kamyon Tespit Edildi")
                return 1
        return 0
    




