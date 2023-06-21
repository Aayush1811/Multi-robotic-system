from inspect import Parameter
from multiprocessing.spawn import import_main_path
import cv2 as cv
import numpy as np
from cv2 import aruco 
import math
from glob import glob
import paho.mqtt.client as mqttclient 
import time
import math
from tkinter import *

xp = 0
shape = 0
size = 0
count = 0
s=0
angle = 0

integral = 0
prev_error = 0

mx_1 = 0
mx_2 = 0
mx_3 = 0
mx_4 = 0

my_1 = 0
my_2 = 0
my_3 = 0
my_4 = 0

set_x1 = 0
set_x2 = 0
set_x3 = 0
set_x4 = 0
set_y1 = 0
set_y2 = 0
set_y3 = 0
set_y4 = 0



def on_connect(client,userdata,flag,rc):
    if rc == 0:
        print("client is connectd")
        global connected
        connected = True
        

    else:
        print("client is not connected")
        
def on_message(client,userdata,message):
    messagearrieved = True
    global s
    s = message.payload.decode("utf-8")
    s = str(s)
    
        
connected = False
messagearrieved = False

#brokeradd = "64:ff9b::12c4:a6b5"
brokeradd = "broker.mqtt-dashboard.com"
port = 1883

client = mqttclient.Client("MQTT")
client.on_connect=on_connect
client.on_message=on_message
client.connect(brokeradd,port=port)
client.loop_start()
client.subscribe("shape")
client.subscribe("bot_2")



marker_dict = aruco.Dictionary.get(aruco.DICT_4X4_50)
marker_param = aruco.DetectorParameters_create()

#-------------------------------------------------------------------------------------------------------------
#=============================================================================================================
def square(id,corner,frame,m_corner,m_id):
    
    global count
    #print(id)
    for id,corner in zip(m_id,m_corner):

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
                
                global size
                
                if(size == 20):
                    #300
                    #print("size: {}".format(size))
                    A1 = 100
                    B1 = 100
                    A2 = 400
                    B2 = 100
                    A3 = 400
                    B3 = 400
                    A4 = 100
                    B4 = 400
                if(size == 50):
                    #600
                    #print("size: {}".format(size))
                    
                    A1 = 100
                    B1 = 100
                    A2 = 700
                    B2 = 100
                    A3 = 700
                    B3 = 700
                    A4 = 100
                    B4 = 700
                if(size == 100):
                    #print("size: 100")
                    
                    # 100
                    A1 = 100
                    B1 = 100
                    A2 = 200
                    B2 = 100
                    A3 = 200
                    B3 = 200
                    A4 = 100
                    B4 = 200
                if(size == 200):
                    #print("size: 200")
                    
                    # 500
                    A1 = 100
                    B1 = 100
                    A2 = 600
                    B2 = 100
                    A3 = 600
                    B3 = 600
                    A4 = 100
                    B4 = 600
                
                SET = [(A1,B1),(A2,B2),(A3,B3),(A4,B4)]
                if(count<=3):
                    print("id: ",id)
                    
                        
                    #cv.circle(frame,(x3,y3),5,(0,0,255),-1)
                    if(id == 4):
                        id_4 = 4
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                    
                    
                        # mid point of upper line of aruco
                        l1 = (x1+x2)/2 # x-coordinate
                        l2 = (y1+y2)/2 # y coordinate
                    
                        # mid points of aruco
                        m1 = (a1+a3)/2 # x-coordinate
                        m2 = (a2+a4)/2 # y coordinate
                        global mx_4
                        global my_4
                        
                        mx_4 = int(m1)
                        my_4 = int(m2)              
                    
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),5,(255,0,0),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(0,0,255),2)
                        #cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                    
                        
                        pos = f'bot_4 = ({int(m1)},{int(m2)})'
                        #distance = f'{dis}'
                        #distance_l = f'{dis_l}'
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        #cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point

                        #cv.putText(frame,pos,(1050,89),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"4",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    if(id == 3):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        
                    
                        # mid point of upper line of aruco
                        l1 = (x1+x2)/2 # x-coordinate
                        l2 = (y1+y2)/2 # y coordinate
                    
                        # mid points of aruco
                        m1 = (a1+a3)/2 # x-coordinate
                        m2 = (a2+a4)/2 # y coordinate
                    
                        global mx_3
                        global my_3
                        mx_3 = int(m1)
                        my_3 = int(m2) 
                    
                                    
                    
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),5,(255,0,0),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(0,0,255),2)
                        #cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                        pos = f'bot_3 = ({int(m1)},{int(m2)})'
                        
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        #cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        #cv.putText(frame,pos,(1050,66),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"3",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    
                    if(id == 1):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        
                    
                        # mid point of upper line of aruco
                        l1 = (x1+x2)/2 # x-coordinate
                        l2 = (y1+y2)/2 # y coordinate
                    
                        # mid points of aruco
                        m1 = (a1+a3)/2 # x-coordinate
                        m2 = (a2+a4)/2 # y coordinate
                    
                        global mx_1
                        global my_1
                        
                        mx_1 = int(m1)
                        my_1 = int(m2) 
                        
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),5,(255,0,0),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(0,0,255),2)
                        #cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                        pos = f'bot_1 = ({int(m1)},{int(m2)})'
                        
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        #cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        #cv.putText(frame,pos,(1050,20),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"1",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        
                    if(id == 2):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        
                    
                        # mid point of upper line of aruco
                        l1 = (x1+x2)/2 # x-coordinate
                        l2 = (y1+y2)/2 # y coordinate
                    
                        # mid points of aruco
                        m1 = (a1+a3)/2 # x-coordinate
                        m2 = (a2+a4)/2 # y coordinate
                    
                        global mx_2
                        global my_2
                        mx_2 = int(m1)
                        my_2 = int(m2) 
                                    
                    
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),8,(0,255,255),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(255,0,255),2)
                        #cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                        pos = f'bot_2 = ({int(m1)},{int(m2)})'
                        
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        #cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        #cv.putText(frame,pos,(1050,43),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"2",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    
                    count = count +1
                
                
                
                if(count == 4):
                    print("({},{})".format(mx_1,my_1))
                    print("({},{})".format(mx_2,my_2))    
                    print("({},{})".format(mx_3,my_3))    
                    print("({},{})".format(mx_4,my_4))    
                    count = count +1
                
                # -------------------------------------------------------------------
                # OPTIMIM PATH FIND ALGORITM:    
                # -------------------------------------------------------------------
                
                if(count == 5):
                    
                    global set_x1
                    global set_x2
                    global set_x3
                    global set_x4
                    global set_y1
                    global set_y2
                    global set_y3
                    global set_y4
                    
                    
                    d1 = math.sqrt( pow(mx_1-SET[0][0],2) + pow(my_1-SET[0][1],2))
                    d2 = math.sqrt( pow(mx_1-SET[1][0],2) + pow(my_1-SET[1][1],2))
                    d3 = math.sqrt( pow(mx_1-SET[2][0],2) + pow(my_1-SET[2][1],2))
                    d4 = math.sqrt( pow(mx_1-SET[3][0],2) + pow(my_1-SET[3][1],2))
                    print("d1:",d1)
                    print("d2:",d2)
                    print("d3:",d3)
                    print("d4:",d4)
                        
                        
                    l = [d1,d2,d3,d4]
                    dis_min1 = min(l)
                    index1 = l.index(dis_min1)
                    print(index1)
                        
                    if(index1 == 0):
                        set_x1 = A1
                        set_y1 = B1
                    if(index1 == 1):
                        set_x1 = A2
                        set_y1 = B2
                    if(index1 == 2):
                        set_x1 = A3
                        set_y1 = B3
                    if(index1 == 3):
                        set_x1 = A4
                        set_y1 = B4
                            
                            
                    SET.pop(index1)
                    print("id_1")
                    print("({},{})".format(set_x1,set_y1))
                    print(SET)
                    
                    d1 = math.sqrt( pow(mx_2-SET[0][0],2) + pow(my_2-SET[0][1],2))
                    d2 = math.sqrt( pow(mx_2-SET[1][0],2) + pow(my_2-SET[1][1],2))
                    d3 = math.sqrt( pow(mx_2-SET[2][0],2) + pow(my_2-SET[2][1],2))
                        
                    print("d1:",d1)
                    print("d2:",d2)
                    print("d3:",d3)
                        
                        
                        
                    l = [d1,d2,d3]
                    dis_min2 = min(l)
                    index2 = l.index(dis_min2)
                    print(index2)
                    
                        
                    if(index2 == 0):
                        set_x2 = SET[0][0]
                        set_y2 = SET[0][1]
                    if(index2 == 1):
                        set_x2 = SET[1][0]
                        set_y2 = SET[1][1]
                    if(index2 == 2):
                        set_x2 = SET[2][0]
                        set_y2 = SET[2][1]
                        
                            
                            
                    SET.pop(index2)
                    print("id_2")
                    print("({},{})".format(set_x2,set_y2))
                    print(SET)
                    
                    d1 = math.sqrt( pow(mx_3-SET[0][0],2) + pow(my_4-SET[0][1],2))
                    d2 = math.sqrt( pow(mx_3-SET[1][0],2) + pow(my_4-SET[1][1],2))
                    
                        
                    print("d1:",d1)
                    print("d2:",d2)
                    
                        
                        
                        
                    l = [d1,d2]
                    dis_min3 = min(l)
                    index3 = l.index(dis_min3)
                    print(index3)
                    
                        
                    if(index3 == 0):
                        set_x3 = SET[0][0]
                        set_y3 = SET[0][1]
                    if(index3 == 1):
                        set_x3 = SET[1][0]
                        set_y3 = SET[1][1]
                    
                        
                            
                            
                    SET.pop(index3)
                    print("id_3")
                    print("({},{})".format(set_x3,set_y3))
                    print(SET)
                    
                    set_x4 = SET[0][0]
                    set_y4 = SET[0][1]
                    print("({},{})".format(set_x4,set_y4))
                    
                    count = count + 1
                        
                
                if(count>5):
                    if(id == 4):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        # set points
                        set1 = set_x4
                        set2 = set_y4
                    
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
                        
                        print(dis)
                        
                        cm = dis/8.82
                        print(cm) 
                    
                        D1 = pow((set1-l1),2)
                        D2 = pow((set2-l2),2) 
                        dis_l = math.sqrt(D1+D2)  
                        
                        # dis === distance btw set point and mid point
                        # dis_l === angle btw set point and front part of code            
                    
                    
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
                        
                        angle = f'bot_1: {degree}'
                        pos = f'bot_4 = ({int(m1)},{int(m2)})'
                        distance = f'{dis}'
                        distance_l = f'{dis_l}'
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point

                        cv.putText(frame,pos,(1050,89),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"4",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        
                        
                        
                        client.publish("bot4",degree)
                        client.publish("bot4",dis)
                        client.publish("bot4",dis_l)
                        
                        
                        
                        #client.publish("bot3",dis_l)
                        
                        
                        
                    if(id == 3):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        # set points
                        set1 = set_x3
                        set2 = set_y3
                    
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

                        print(dis)
                        
                        cm = dis/8.82
                        print(cm)
                        
                        D1 = pow((set1-l1),2)
                        D2 = pow((set2-l2),2) 
                        dis_l = math.sqrt(D1+D2)              
                    
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),5,(255,0,0),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(0,0,255),2)
                        cv.line(frame,(int(m1),int(m2)),(set1,set2),(0,0,255),2)
                    
                        slop_line_constant = math.atan2((m1-l1),(m2-l2))
                        slop_line_set = math.atan2((set1-m1),(set2-m2))
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
                        
                        angle = f'bot_1: {degree}'
                        pos = f'bot_3 = ({int(m1)},{int(m2)})'
                        distance = f'{dis}'
                        distance_l = f'{dis_l}'
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        cv.putText(frame,pos,(1050,66),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"3",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        
                        client.publish("bot2",degree)
                        client.publish("bot2",dis)
                        
                    
                    if(id == 1):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        # set points
                        set1 = set_x1
                        set2 = set_y1
                    
                        # mid point of upper line of aruco
                        l1 = (x1+x2)/2 # x-coordinate
                        l2 = (y1+y2)/2 # y coordinate
                    
                        # mid points of aruco
                        m1 = (a1+a3)/2 # x-coordinate
                        m2 = (a2+a4)/2 # y coordinate
                    
                    
                        d1 = pow((set1-m1),2)
                        d2 = pow((set2-m2),2)
                        dis = math.sqrt(d1+d2)
                        print(dis)
                        
                        cm = dis/8.82
                        print(cm)
                         
                    
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
                        
                        angle = f'bot_1: {degree}'
                        pos = f'bot_1 = ({int(m1)},{int(m2)})'
                        distance = f'{dis}'
                        distance_l = f'{dis_l}'
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        cv.putText(frame,pos,(1050,20),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"1",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        
                        client.publish("bot1",degree)
                        #client.publish("bot1",dis)
                        
                    if(id == 2):
                        # 1st, 2nd & 3rd point of aruco
                        a1 = x1
                        a2 = y1
                        a3 = x3
                        a4 = y3
                        a5 = x2
                        a6 = y2
                    
                        # set points
                        set1 = set_x2
                        set2 = set_y2
                    
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
                        print(dis)
                        
                        cm = dis/8.71
                        print(cm)
                    
                        D1 = pow((set1-l1),2)
                        D2 = pow((set2-l2),2) 
                        dis_l = math.sqrt(D1+D2)              
                    
                    
                        #cv.circle(frame,(int(m1),int(m2)),5,(0,0,255),-1)
                        cv.circle(frame,(int(l1),int(l2)),8,(0,255,255),-1)
                        cv.circle(frame,(int(m1),int(m2)),5,(255,0,0),-1)
                    
                        cv.line(frame,(int(m1),int(m2)),(int(l1),int(l2)),(255,0,255),2)
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
                        
                        angle = f'bot_1: {degree}'
                        pos = f'bot_2 = ({int(m1)},{int(m2)})'
                        distance = f'{dis}'
                        distance_l = f'{dis_l}'
                                
                        #return angle,pos,distance,m1,m2,set1,set2
                        #cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                        #cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                        #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                        cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                        #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                        cv.putText(frame,pos,(1050,43),cv.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),1)
                        cv.rectangle(frame,(a1,a2-40),(a1+30,a2-7),(255,0,0),-1)
                        cv.putText(frame,"2",(a1,a2-10),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                        
                        client.publish("robot",degree)
                        client.publish("robot",dis)
                        
                        
                
                    
                        
                    
                    
                    
                    
#-------------------------------------------------------------------------------------------------------------
#=============================================================================================================
def triangle(id,corner,frame,m_corner,m_id):
    for id,corner in zip(m_id,m_corner):

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
                    set2 = 100
                
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
                        
                    
                    angle = f'bot_1: {degree}'
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    
                    ref = dis_l - dis
                    client.publish("bot1",degree)
                    #client.publish("bot1_r",ref) 
                    
                if(id == 2):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 200
                    set2 = 700
                
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
                        
                    
                    angle = f'bot_1: {degree}'
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                
                    cv.putText(frame,angle,(30,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    
                    ref = dis_l - dis
                    client.publish("bot_1",degree)
                    #client.publish("bot1_r",ref) 
                    
                if(id == 3):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 800
                    set2 = 700
                
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
                        
                    
                    angle = f'bot_1: {degree}'
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    
                    ref = dis_l - dis
                    client.publish("bot_1",pos)
                    #client.publish("bot1_r",ref) 

#-------------------------------------------------------------------------------------------------------------
#=============================================================================================================
def line(id,corner,frame,m_corner,m_id):
    for id,corner in zip(m_id,m_corner):

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
                
                if(id == 5):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 100
                    set2 = 700
                
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
                        
                    
                    angle = f'bot_1: {degree}'
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    
                    ref = dis_l - dis
                    client.publish("bot1",degree)
                    #client.publish("bot1_r",ref)
                    
                    
                    
                    
                if(id == 6):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 1000
                    set2 = 100
                
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
                        
                    
                    angle = f'bot_2: {degree}'
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                
                    cv.putText(frame,angle,(30,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    
                    ref = dis_l - dis
                    client.publish("bot2",degree)
                    #client.publish("bot1_r",ref)  
                    
                    
                    
# ------------------------------------------------------------------------------------------------------------
# ============================================================================================================

def custom(id,corner,frame,m_corner,m_id):
    print('hello')
    print("point_1 : ({},{})".format(t1,t2))
    print("point_2 : ({},{})".format(t3,t4))
    print("point_3 : ({},{})".format(t5,t6))
    print("point_4 : ({},{})".format(t7,t8))



from tkinter import *

root = Tk()

#root1.title('CUSTOMISED_SHAPE')
root.geometry("800x500")
x = 0
t1 = 0

# SHAPE FUNCTIONS
# SHAPE FUNCTIONS
def sq():
    global shape
    shape = 'square'
def tri():
    global shape
    shape = 'tri'
def li():
    global shape
    shape = 'line'
    global x
    
    if(x == 0):
        v = Label(root,text=' ')
        v.pack()
        vline = Button(root,text='vline',font='impact 20',fg='white',height=1,width=5,relief='groove',borderwidth=10,bg='grey')
        vline.pack(side=TOP)
        hline = Button(root,text='hline',font='impact 20',fg='white',height=1,width=5,relief='groove',borderwidth=10,bg='grey')
        hline.pack()
        x= x+1   
def rec():
    print("RECTANGLE")    
    
def cus():
    
    global shape
    shape = 'custom' 
    print(shape)  
    root1 = Toplevel(root)
    root1.title('A')
    
    
    root1.geometry("500x400")
    def sub():
        global t1
        global t2
        global t3
        global t4
        global t5
        global t6
        global t7
        global t8
        
        
        t1 = v1.get()
        t2 = v2.get()
        t3 = v3.get()
        t4 = v4.get()
        t5 = v5.get()
        t6 = v6.get()
        t7 = v7.get()
        t8 = v8.get()
        
        
    def cam():
        # MAIN PROGRRAME
        cap = cv.VideoCapture(1)
        cap.set(3,2000)
        cap.set(4,2000)
        
        while(True):
            #print(shape)
            #print(size)
            #print(s)
            ret,frame = cap.read()
            gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            
            m_corner,m_id,rej = aruco.detectMarkers(gray, marker_dict, parameters=marker_param)
            #print(m_id)
            h,w,c = frame.shape
            #cv.line(frame,(0,10),(w,10),(255,0,0),3)
            
            
            if(m_corner):
                id = m_id.astype(int) 
                #print(id)
                for id,corner in zip(m_id,m_corner):

                        id = int(id)
                        corner = corner.astype(int)
                        #print(id)
                        cv.polylines(frame,corner,True,(0,255,0),3)
                
                
                # s is stroring message given from user in mqtt
                # it will indicating shape
                # according to shape it will go in diff func and alloted set point accordig to shape        
                custom(id,corner,frame,m_corner,m_id)
                    
                
                    
            
            
            cv.imshow('f',frame)
            key = cv.waitKey(1)
            if(key == ord('a')):
                break
            
        cap.release()
        client.loop_stop()
        cv.destroyAllWindows()
      
        
    
    # point 1
    l1 = Label(root1,text='point_1', font='12', bg='#a0ced9',fg='black')
    l1.grid(row=0, column=0)
    
    x1 = Label(root1, text='x1: ' , font = '12',pady=5,padx = 20)
    x1.grid(row=1,column=0)
    x2 = Label(root1, text='x2: ' , font = '12')
    x2.grid(row=2,column=0)
    
    #global val1
    
    v1 = IntVar()
    v2 = IntVar()
    
     
    p1 = Entry(root1,  width=30, borderwidth=4, bg='#d1d1d1',textvariable=v1)
    p1.grid(row=1,column=1)
    p2 = Entry(root1, textvariable=v2, width=30, borderwidth=4, bg='#d1d1d1')
    p2.grid(row=2,column=1)
    
    # point 2
    ll = Label(root1, text='  ')
    ll.grid(row=3)
    l2 = Label(root1,text='point_2', font='12', bg='#a0ced9',fg='black')
    l2.grid(row=4, column=0)
    
    x3 = Label(root1, text='x3: ' , font = '12',pady=5,padx = 20)
    x3.grid(row=5,column=0)
    x4 = Label(root1, text='x4: ' , font = '12')
    x4.grid(row=6,column=0)
    
    v3 = IntVar()
    v4 = IntVar()
    
    p3 = Entry(root1, textvariable=v3, width=30, borderwidth=4, bg='#d1d1d1')
    p3.grid(row=5,column=1)
    p4 = Entry(root1, textvariable=v4,width=30, borderwidth=4, bg='#d1d1d1')
    p4.grid(row=6,column=1)
    
    #point_3
    ll_1 = Label(root1, text='  ')
    ll_1.grid(row=7)
    l3 = Label(root1,text='point_3', font='12', bg='#a0ced9',fg='black')
    l3.grid(row=8, column=0)
    
    x5 = Label(root1, text='x5: ' , font = '12',pady=5,padx = 20)
    x5.grid(row=9,column=0)
    x6 = Label(root1, text='x6: ' , font = '12')
    x6.grid(row=10,column=0)
    
    v5 = IntVar()
    v6 = IntVar()
    
    p5 = Entry(root1, textvariable=v5, width=30, borderwidth=4, bg='#d1d1d1')
    p5.grid(row=9,column=1)
    p6 = Entry(root1, textvariable=v6,width=30, borderwidth=4, bg='#d1d1d1')
    p6.grid(row=10,column=1)
    
    # point 4
    ll_2 = Label(root1, text='  ')
    ll_2.grid(row=11)
    l4 = Label(root1,text='point_4', font='12', bg='#a0ced9',fg='black')
    l4.grid(row=12, column=0)
    
    x7= Label(root1, text='x7: ' , font = '12',pady=5,padx = 20)
    x7.grid(row=13,column=0)
    x8 = Label(root1, text='x8: ' , font = '12')
    x8.grid(row=14,column=0)
    
    v7 = IntVar()
    v8 = IntVar()
    
    p7 = Entry(root1, textvariable=v7, width=30, borderwidth=4, bg='#d1d1d1')
    p7.grid(row=13,column=1)
    p8 = Entry(root1, textvariable=v8,width=30, borderwidth=4, bg='#d1d1d1')
    p8.grid(row=14,column=1)
    
    l7 = Label(root1, text='                            ')
    l7.grid(row=6,column=3)
    B = Button(root1, text='submit',relief='groove',width=8,height=2,borderwidth=4, command=sub)
    B.grid(row=5,column=6)
    B1 = Button(root1, text='Camara_on',relief='groove',width=8,height=2,borderwidth=4,command=cam)
    B1.grid(row=7,column=6)
    
    
   
    

# SIZE FUNCTIONS    
# SIZE FUNCTIONS    
def s_20():
    global size
    size = 20
    #print(size)
def s_50():
    global size
    size = 50
    #print(size)
    
def s_100():
    global size
    size = 100
    #print(size)
    
def s_200():
    global size
    size = 200  
    #print(size)
      
     
def setval():
    
   # MAIN PROGRRAME
   # "http://192.168.80.21:4747/video"
    cap = cv.VideoCapture(1)
    cap.set(3,2000)
    cap.set(4,2000)
    while(True):
        #print(shape)
        #print(size)
        #print(s)
        ret,frame = cap.read()
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
        m_corner,m_id,rej = aruco.detectMarkers(gray, marker_dict, parameters=marker_param)
        #print(m_id)
        h,w,c = frame.shape
        #cv.line(frame,(0,10),(w,10),(255,0,0),3)
        
        
        if(m_corner):
            id = m_id.astype(int) 
            #print(id)
            for id,corner in zip(m_id,m_corner):

                    id = int(id)
                    corner = corner.astype(int)
                    #print(id)
                    cv.polylines(frame,corner,True,(0,255,0),3)
            
            
            # s is stroring message given from user in mqtt
            # it will indicating shape
            # according to shape it will go in diff func and alloted set point accordig to shape        
            if(shape == "square"):
                square(id,corner,frame,m_corner,m_id)
            if(shape == 'tri'):
                triangle(id,corner,frame,m_corner,m_id)
            if(shape == 'line'):
                line(id,corner,frame,m_corner,m_id)
            #if(shape == 'custom'):
                
            
                
        
        
        cv.imshow('f',frame)
        key = cv.waitKey(1)
        if(key == ord('a')):
            client.publish("bot_stop","pwm = 0")
            break
        
    cap.release()
    client.loop_stop()
    cv.destroyAllWindows()
    

l_shape = Label(text='SHAPE', font="IMPACT 15", bg='red', fg='white', padx=5, pady=5)
l_shape.pack()
l11 = Label(text=' ')
l11.pack()

f1 = Frame(root, borderwidth=8 , relief="sunken",padx=5, pady=10 )
f1.pack(side=TOP)


l2 = Label(text=' ')
l2.pack()
l3 = Label(text=' ')
l3.pack()

l_size = Label(text='SIZE', font="IMPACT 15", bg='red', fg='white', padx=5, pady=5)
l_size.pack()
l22 = Label(text=' ')
l22.pack()

f2 = Frame(root, borderwidth=8 , relief='sunken', pady=10 )
f2.pack(side=TOP)



# shape
b1 = Button(f1,text='SQUARE',font='impact 20', bg='gray' , command=sq, padx=15,pady=5)
b1.pack(side=LEFT,padx=5)

b2 = Button(f1,text='TRIANGLE',font='impact 20', bg='gray' , command=tri, padx=13,pady=5)
b2.pack(side=LEFT,padx=5)

b3 = Button(f1,text='LINE',font='impact 20', bg='gray' , command=line, padx=35,pady=5)
b3.pack(side=LEFT,padx=5)

b4 = Button(f1,text='RECTANGLE',font='impact 20', bg='gray' , command=rec, padx=5,pady=5)
b4.pack(side=LEFT,padx=5)

b = Button(f1,text='Custom',font='impact 20', bg='gray' , command=cus, padx=5,pady=5)
b.pack(side=LEFT,padx=5)

# size
b5 = Button(f2,text='20',borderwidth=10,font='impact 25 bold', bg='#adf7b6' , command=s_20, padx=45,pady=5,relief='groove')
b5.pack(side=LEFT,padx=8)

b6 = Button(f2,text='50',borderwidth=10,font='impact 25 bold', bg='#ffee93' , command=s_50, padx=47,pady=5,relief='groove')
b6.pack(side=LEFT,padx=5)

b7 = Button(f2,text='100',borderwidth=10,font='impact 25 bold', bg='#ffc09f' , command=s_100, padx=40, pady=5,relief='groove')
b7.pack(side=LEFT,padx=5)

b8 = Button(f2,text='200',borderwidth=10,font='impact 25 bold', bg='#a0ced9' , command=s_200, padx=40, pady=5,relief='groove')
b8.pack(side=LEFT,padx=5)

l33 = Label(text=' ')
l33.pack()

b9 = Button(text='SET',font='impact 15',fg='black',borderwidth=15, relief='groove',padx=5, command=setval)
b9.pack(side=TOP)

root.mainloop()