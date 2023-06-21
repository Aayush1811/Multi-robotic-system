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


s=0
angle = 0

integral = 0
prev_error = 0

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
brokeradd = "64:ff9b::3439:818c"
port = 1883

client = mqttclient.Client("MQTT")
client.on_connect=on_connect
client.on_message=on_message
client.connect(brokeradd,port=port)
client.loop_start()
client.subscribe("shape")

cap = cv.VideoCapture(1)
cap.set(3,2000)
cap.set(4,2000)

marker_dict = aruco.Dictionary.get(aruco.DICT_4X4_50)
marker_param = aruco.DetectorParameters_create()

#-------------------------------------------------------------------------------------------------------------
#=============================================================================================================
def square(id,corner,frame,m_corner,m_id):
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
            
                #cv.circle(frame,(x3,y3),5,(0,0,255),-1)
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
                            
                    #return angle,pos,distance,m1,m2,set1,set2
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                
                if(id == 6):
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
                    pos = f'pos = ({int(m1)},{int(m2)})'
                    distance = f'{dis}'
                    distance_l = f'{dis_l}'
                            
                    #return angle,pos,distance,m1,m2,set1,set2
                    
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                
                
                if(id == 1):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 700
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
                            
                    #return angle,pos,distance,m1,m2,set1,set2
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point

                if(id == 2):
                    # 1st, 2nd & 3rd point of aruco
                    a1 = x1
                    a2 = y1
                    a3 = x3
                    a4 = y3
                    a5 = x2
                    a6 = y2
                
                    # set points
                    set1 = 700
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
                            
                    #return angle,pos,distance,m1,m2,set1,set2
                    cv.putText(frame,angle,(30,30),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                    cv.putText(frame,pos,(int(m1),int(m2-10)),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    #cv.putText(frame,distance,(60,60),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from mid
                    cv.circle(frame,(set1,set2),5,(255,0,0),-1)
                    #cv.putText(frame,distance_l,(60,100),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)# distance from edge point
                                
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
                
                if(id == 5):
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
                    
                if(id == 6):
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
                    client.publish("bot2",degree)
                    #client.publish("bot1_r",ref) 
                    
                if(id == 1):
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
                    client.publish("bot1",degree)
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


# MAIN PROGRRAME
while(True):
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
        if(s == "square"):
            square(id,corner,frame,m_corner,m_id)
        if(s == 'tri'):
            triangle(id,corner,frame,m_corner,m_id)
        if(s == 'line'):
            line(id,corner,frame,m_corner,m_id)
        
            
    
    
    cv.imshow('f',frame)
    key = cv.waitKey(1)
    if(key == ord('a')):
        break
    
cap.release()
client.loop_stop()
cv.destroyAllWindows()