from inspect import Parameter
from multiprocessing.spawn import import_main_path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from cv2 import aruco 
import math
from glob import glob
import paho.mqtt.client as mqttclient 
import time
import math


# COMMUNICATION CODE

def on_connect(client,userdata,flag,rc):
    if rc == 0:
        print("client is connectd")
        global connected
        connected = True
        

    else:
        print("client is not connected") 
        
connected = False
messagearrieved = False

#brokeradd = "64:ff9b::12c4:a6b5"
brokeradd = "3.73.104.160"
port = 1883

client = mqttclient.Client("MQTT")
client.on_connect=on_connect
client.connect(brokeradd,port=port)
client.loop_start()

client.subscribe("shape")

cap = cv.VideoCapture(0)
cap.set(3,2000)
cap.set(4,2000)

marker_dict = aruco.Dictionary.get(aruco.DICT_4X4_50)
marker_param = aruco.DetectorParameters_create()

while(True):
    ret,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    
    m_corner,m_id,rej = aruco.detectMarkers(gray, marker_dict, parameters=marker_param)
    #print(m_id)
    
    h,w,c = frame.shape
    #cv.line(frame,(0,10),(w,10),(255,0,0),3)
    
    if(m_corner):
        id = m_id.astype(int) 
        print(id)
        # m_id include all detected id 
    
        
        for id,corner in zip(m_id,m_corner):
            
            # it will take all id individually from that detected id
            id = int(id)
            corner = corner.astype(int)
            #print(id)
            cv.polylines(frame,corner,True,(0,255,0),3)
            
            x1 = corner.ravel()[0]  #--> invoking 1st num in array        
            y1 = corner.ravel()[1]  
            x2 = corner.ravel()[2]
            y2 = corner.ravel()[3]
            x3 = corner.ravel()[4]
            y3 = corner.ravel()[5]
            x4 = corner.ravel()[6]
            y4 = corner.ravel()[7]
            
            #cv.circle(frame,(x3,y3),5,(0,0,255),-1)
            
            # according to id number define specific id parameters
            if(id == 1):
                # 1st, 2nd & 3rd point of aruco
                a1 = x1
                a2 = y1
                a3 = x3
                a4 = y3
                a5 = x2
                a6 = y2
                
                # set points
                set1 = 500
                set2 = 300
                
                # mid point of upper line of aruco
                l1 = (x1+x2)/2 # x-coordinate
                l2 = (y1+y2)/2 # y coordinate
                
                # mid points of aruco
                m1 = (a1+a3)/2 # x-coordinate
                m2 = (a2+a4)/2 # y coordinate
                
                
                d1 = pow((set1-m1),2)
                d2 = pow((set2-m2),2)
                dis = math.sqrt(d1+d2)
                #print(dis) 
                
                D1 = pow((set1-l1),2)
                D2 = pow((set2-l2),2) 
                dis_l = math.sqrt(D1+D2)              
                
                
                #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                cv.circle(frame,(int(l1),int(l2)),5,(255,0,0),-1)
                cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                
                cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(0,0,255),2)
                cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                
                slop_line_constant = (m2-l2)/(m1-l1)
                slop_line_set = (set2-m2)/(set1-m1)
                A = slop_line_constant
                B = slop_line_set
                #print(m2)
                
                
                if(A*B == -1):
                    degree = 90
                
                else:
                    tan = (B-A)/(1+(A*B))
                    #print(tan)
                    angle = math.atan(tan)    # angle in rad
                    degree = -(57.296*angle)  # angle in degree
                    #print(degree)
                
                    if(degree<0):
                        degree = 180+degree
                        
                    
                          
                    
                
                text = f'{degree}'
                t = f'pos = ({int(m1)},{int(m2)})'
                distance = f'{dis}'
                distance_l = f'{dis_l}'
                
                
                cv.putText(frame,text,(set2-10,set1-10),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
                #cv.putText(frame,t,(int(m1)+20,int(m2)+20),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                cv.putText(frame,t,(700,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                
                ref = dis_l - dis
                
                #client.publish("bot1",degree)
                #client.publish("bot1_r",ref) 
                #print(dis)
                
                
            text = str(f"id: {id}")
            font = cv.FONT_HERSHEY_COMPLEX
            #cv.putText(frame,text,(x1,y1-5),font,0.5,(0,0,255),1)
                
                
    cv.imshow('f',frame)
    key = cv.waitKey(1)
    if(key == ord('a')):
        break
    
cap.release()
client.loop_stop()
cv.destroyAllWindows()