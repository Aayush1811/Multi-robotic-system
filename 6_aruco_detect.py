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

def on_connect(client,userdata,flag,rc):
    if rc == 0:
        print("client is connectd")
        global connected
        connected = True

    else:
        print("client is not connected") 
        
connected = False
messagearrieved = False

brokeradd = "64:ff9b::349:68a0"
port = 1883

client = mqttclient.Client("MQTT")
client.on_connect=on_connect
client.connect(brokeradd,port=port)
client.loop_start()
 
# "http://192.168.161.200:4747/video"
cap = cv.VideoCapture(0)
cap.set(3,500)
cap.set(4,1280)

marker_dict = aruco.Dictionary.get(aruco.DICT_4X4_50)
marker_param = aruco.DetectorParameters_create()

inc12 = 0
inc13 = 0
inc14 = 0
inc15 = 0

count_for12 = 0
count_for13 = 0
count_for14 = 0
count_for15 = 0
id12 = 0


while(cap.isOpened()==True):
    
    idd1 = id12
    idd2 = id12
    
    
    ret,frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    
    
    
    
    m_corner,m_id,rej = aruco.detectMarkers(gray, marker_dict, parameters=marker_param)
    #print(m_id)
    
    h,w,c = frame.shape
    print("w: {}".format(w))
    print("h: {}".format(h))
    
    cv.line(frame,(0,10),(w,10),(255,0,0),3)
    cv.circle(frame,(h,w),10,-1)

    m1 = 0
    #print(frame.shape)
    
    if(m_corner):
        id = m_id.astype(int) 
        #print(id)
        num_id = len(id)
        #print("number of id detected: ",num_id)

        
        id_1 = 0
        id_2 = 0
        id_3 = 0
        id_4 = 0
        id_5 = 0
        id_6 = 0
        id_11 = 0
        
        
        

        for id,corner in zip(m_id,m_corner):

            id = int(id)
            corner = corner.astype(int)

            cv.polylines(frame,corner,True,(0,255,0),3)
            
                
            #print('corners: ',corner.ravel())
            x1 = corner.ravel()[0]  #--> invoking 1st num in array        
            y1 = corner.ravel()[1]
            x2 = corner.ravel()[2]
            y2 = corner.ravel()[3]
            x3 = corner.ravel()[4]
            y3 = corner.ravel()[5]
            x4 = corner.ravel()[6]
            y4 = corner.ravel()[7]
            

            text = str(f"id: {id}")
            font = cv.FONT_HERSHEY_COMPLEX
            #cv.putText(frame,text,(x1,y1-5),font,0.5,(0,0,255),1)
                

            if(id == 1):
                x_1 = x1
                y_1 = y1
                x_1a = x3
                y_1a = y3
                
                x_2 = x2
                y_2 = y2
                
                cv.line(frame,(x_1,y_1-20),(x_2,y_2-20),(0,0,255),3)
                
                slop = (y_2 - y_1)/(x_2 - x_1)
                #print(slop)

                mx1 = (x_1+x_1a)/2
                my1 = (y_1+y_1a)/2
                mx1 = int(mx1)
                my1 = int(my1)
                
                s = f'bot1 : ({mx1},{my1})'

                id_1 = id

                text_1 = str(1)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(10,10),(45,45),(255,255,255),-1)
                cv.putText(frame,text_1,(15,40),font,1,(0,0,255),1)
                
                client.publish("bot1",mx1)
                client.publish("bot1",my1)
                print(s)
                
                client.publish("bot2",mx1)
                
                
                    


            if(id == 2):
                x_2 = x1
                y_2 = y1
                x_2a = x3
                y_2a = y3  
                #print('==',x1,y1)
                

                mx2 = (x_2+x_2a)/2
                my2 = (y_2+y_2a)/2
                mx2 = int(mx2)
                my2 = int(my2)  
                
                s = f'bot2 : ({mx2},{my2})'
                
                a = x1
                b = y1-10
                c = x2
                d = y2-10
                r1 = x2
                r2 = y2
                r3 = x3
                r4 = y3
                rx = (r1+r3)/2
                ry = (r2+r4)/2
                
                # DETECTING THE ANGLE 
                ref = ry - my2
                
                cv.line(frame,(a,b),(c,d),(0,0,255),3)
                m2 = (b-d)/(a-c)
                
                if(ref <= 0):

                    tan = (m1 - m2)/(1 + m1*m2)     # give tanx value
                    rad = math.atan(tan)
                    deg = rad*57.296
                    if(deg<0):
                        temp = 90+deg
                        deg = 90+temp
                
                    angle = str(deg)
                    cv.putText(frame,angle,(a,b-10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    
                    cv.circle(frame,(mx2,my2),3,(0,0,255),-1)
                elif(ref>0):

                    tan = (m1 - m2)/(1 + m1*m2)     # give tanx value
                    rad = math.atan(tan)
                    deg = 180 + (rad*57.296)
                    if(deg>=90 and deg<=180):
                        temp = deg - 90
                        deg = 270 + temp
                    angle = str(deg)
                    cv.putText(frame,angle,(a,b-10),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)

                id_2 = id
                text_2 = str(2)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(50,10),(85,45),(255,255,255),-1)
                cv.putText(frame,text_2,(55,40),font,1,(0,0,255),1)
                
                client.publish("bot2",mx2)
                client.publish("bot2",my2)
                print(s)

            if(id == 3):
                x_3 = x1
                y_3 = y2
                x_3a = x3
                y_3a = y3  

                mx3 = (x_3+x_3a)/2
                my3 = (y_3+y_3a)/2
                mx3 = int(mx3)
                my3 = int(my3)  

                id_3 = id
                text_3 = str(3)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(90,10),(120,45),(255,255,255),-1)
                cv.putText(frame,text_3,(95,40),font,1,(0,0,255),1)

                    
            if(id == 4):

                x_4 = x1
                y_4 = y1
                x_4a = x3
                y_4a = y3
                
                mx4 = (x_4+x_4a)/2
                my4 = (y_4+y_4a)/2
                mx4 = int(mx4)
                my4 = int(my4) 
                
                id_4 = id
                text_4 = str(4)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(125,10),(155,45),(255,255,255),-1)
                cv.putText(frame,text_4,(130,40),font,1,(0,0,255),1)
                
                cv.circle(frame,(a,b),2,(0,255,0),-1)
                cv.circle(frame,(mx4,my4),2,(0,0,255),-1)
                

            if(id == 5):
                x_5 = x1
                y_5 = y1
                x_5a = x3
                y_5a = y3

                mx5 = (x_5+x_5a)/2
                my5 = (y_5+y_5a)/2
                mx5 = int(mx5)
                my5 = int(my5)  

                id_5 = id
                text_5 = str(5)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(160,10),(190,45),(255,255,255),-1)
                cv.putText(frame,text_5,(165,40),font,1,(0,0,255),1)

            if(id == 6):
                x_6 = x1
                y_6 = y1
                x_6a = x3
                y_6a = y3

                mx6 = (x_6+x_6a)/2
                my6 = (y_6+y_6a)/2
                mx6 = int(mx6)
                my6 = int(my6)  

                id_6 = id
                
                text_6 = str(6)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.rectangle(frame,(195,10),(225,45),(255,255,255),-1)
                cv.putText(frame,text_6,(200,40),font,1,(0,0,255),1)

                #cv.circle(frame,(x1,y1),4,(0,0,255),-1)   # top left
                #cv.circle(frame,(x2,y2),4,(0,0,255),-1)   # top right
                #cv.circle(frame,(x3,y3),4,(0,0,255),-1)   # bottom right
                #cv.circle(frame,(x4,y4),4,(0,0,255),-1)   # bottom left

            
            # if id1 and id2 are detected
            if(id_1 and id_2):
                
                id12 = 1
                idd2 = id12
                
                cv.line(frame,(mx1,my1),(mx2,my2),(0,0,255),1)
                cv.circle(frame,(mx1,my1),3,(0,0,255),-1)
                cv.circle(frame,(mx2,my2),3,(0,0,255),-1)

                # finding mid point of line
                mid_of_line_x12 = (mx1+mx2)/2
                mid_of_line_y12 = (my1+my2)/2

                mid_of_line_x12 = int(mid_of_line_x12)
                mid_of_line_y12 = int(mid_of_line_y12)

                # finding length of distance

                l_x12 = pow((mx1-mx2),2)
                l_y12 = pow((my1-my2),2)
                dis12 = math.sqrt(l_x12+l_y12)
                dis12 = int(dis12)
                #print(dis)
                
                c_dis = dis12/37.795275591
                c_dis = int(c_dis)
            
                text = str(c_dis)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(frame,text,(mid_of_line_x12,mid_of_line_y12-5),font,0.5,(255,0,0),1)

                #print("DISTANCE BTW 1 BOT & 2 BOT IS: ",dis12)

                if(inc12 == 0):
                    
                    inc12 = inc12 +1

                if(count_for12 == 0):
                    dis1 = dis12
                    
                if(count_for12 > 0 ):
                    dis2 = dis12
                    if((dis2 - dis1) != 0):
                        
                        client.publish("bot12",dis2)    
                        count_for12 = -1    


                count_for12 = count_for12 + 1
            elif(id_1==0 and id_2==0):
                id12 = 0 
                idd2 = id12 
            else:
                id12 = 0
                idd2 =id12
            
            
                
                

            # if id 1 and 3 are detected
            if(id_1 and id_3):
                cv.line(frame,(mx1,my1),(mx3,my3),(0,0,255),1)
                cv.circle(frame,(mx1,my1),3,(0,0,255),-1)
                cv.circle(frame,(mx3,my3),3,(0,0,255),-1)

                # finding mid point of line
                mid_of_line_x13 = (mx1+mx3)/2
                mid_of_line_y13 = (my1+my3)/2

                mid_of_line_x13 = int(mid_of_line_x13)
                mid_of_line_y13 = int(mid_of_line_y13)

                # finding length of distance

                l_x13 = pow((mx1-mx3),2)
                l_y13 = pow((my1-my3),2)
                dis13 = math.sqrt(l_x13+l_y13)
                dis13 = int(dis13)
                #print(dis)
            
                text = str(dis13)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(frame,text,(mid_of_line_x13,mid_of_line_y13-5),font,0.5,(255,0,0),1)

                #print("DISTANCE BTW 1 BOT & 3 BOT IS: ",dis)

                if(inc13 == 0):
                    client.publish("bot13",dis13)
                    inc13 = inc13 +1

                if(count_for13 == 0):
                    dis1 = dis13
                    
                    
                if(count_for13 > 0 ):
                    dis2 = dis13
                    if(dis2 - dis1 != 0):
                        
                        client.publish("bot13",dis2)    
                        count_for13= -1    


                count_for13 = count_for13 + 1
                
            
            #if id 1 and 4 are detected
            if(id_1 and id_4):
                
                cv.line(frame,(mx1,my1),(mx4,my4),(0,0,255),1)
                cv.circle(frame,(mx1,my1),3,(0,0,255),-1)
                cv.circle(frame,(mx4,my4),3,(0,0,255),-1)
                
                # finding mid point of line
                mid_of_line_x14 = (mx1+mx4)/2
                mid_of_line_y14 = (my1+my4)/2

                mid_of_line_x14 = int(mid_of_line_x14)
                mid_of_line_y14 = int(mid_of_line_y14)

                # finding length of distance

                l_x14 = pow((mx1-mx4),2)
                l_y14 = pow((my1-my4),2)
                dis14 = math.sqrt(l_x14+l_y14)
                dis14 = int(dis14)
                #print(dis14)
            
                text = str(dis14)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(frame,text,(mid_of_line_x14,mid_of_line_y14-5),font,0.5,(255,0,0),1)

                #print("DISTANCE BTW 1 BOT & 4 BOT IS: ",dis)
                
                if(inc14 == 0):
                    client.publish("bot14",f"BTW 1 AND 4 IS:{dis14}")
                    inc14 = inc14 +1

                if(count_for14 == 0):
                    dis1 = dis14
                    
                    
                    
                if(count_for14 > 0 ):
                    dis2 = dis14
                    
                    if(dis2 - dis1 != 0):
                        #print("dis2-dis1",dis2-dis1)
                        client.publish("bot14",f"BTW 1 AND 4 IS:{dis2}")    
                        count_for14= -1    


                count_for14 = count_for14 + 1
                

            

            #if id 1 and 5 are detected
            if(id_1 and id_5):
                cv.line(frame,(mx1,my1),(mx5,my5),(0,0,255),1)
                cv.circle(frame,(mx1,my1),3,(0,0,255),-1)
                cv.circle(frame,(mx5,my5),3,(0,0,255),-1)
                
                # finding mid point of line
                mid_of_line_x15 = (mx1+mx5)/2
                mid_of_line_y15 = (my1+my5)/2

                mid_of_line_x15 = int(mid_of_line_x15)
                mid_of_line_y15 = int(mid_of_line_y15)

                # finding length of distance

                l_x15 = pow((mx1-mx5),2)
                l_y15 = pow((my1-my5),2)
                dis15 = math.sqrt(l_x15+l_y15)
                dis15 = int(dis15)
                #print(dis)
            
                text = str(dis15)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(frame,text,(mid_of_line_x15,mid_of_line_y15-5),font,0.5,(255,0,0),1)

                #print("DISTANCE BTW 1 BOT & 5 BOT IS: ",dis)

                if(inc15 == 0):
                    client.publish("bot15",f"BTW 1 AND 5 IS:{dis15}")
                    inc15 = inc15 +1

                if(count_for15 == 0):
                    dis1 = dis15

                    
                if(count_for15 > 0 ):
                    dis2 = dis15
                    
                    #print("dis2:",dis2)

                    if((dis2 - dis1) != 0):
                        
                        client.publish("bot15",f"BTW 1 AND 5 IS:{dis2}")    
                        count_for15 = -1    


                count_for15 = count_for15 + 1


            #if id 1 and 6 are detected
            if(id_1 and id_6):
                cv.line(frame,(mx1,my1),(mx6,my6),(0,0,255),1)
                cv.circle(frame,(mx1,my1),3,(0,0,255),-1)
                cv.circle(frame,(mx6,my6),3,(0,0,255),-1)
                
                # finding mid point of line
                mid_of_line_x16 = (mx1+mx6)/2
                mid_of_line_y16 = (my1+my6)/2

                mid_of_line_x16 = int(mid_of_line_x16)
                mid_of_line_y16 = int(mid_of_line_y16)

                # finding length of distance

                l_x16 = pow((mx1-mx6),2)
                l_y16 = pow((my1-my6),2)
                dis = math.sqrt(l_x16+l_y16)
                dis = int(dis)
                #print(dis)
            
                text = str(dis)
                font = cv.FONT_HERSHEY_COMPLEX
                cv.putText(frame,text,(mid_of_line_x16,mid_of_line_y16-5),font,0.5,(255,0,0),1)

                #print("DISTANCE BTW 1 BOT & 6 BOT IS: ",dis) 
                
            idd2 = id12
                
            
             
    if(idd1 != idd2):
                print(idd2)  
                client.publish("id",idd2)            

    cv.imshow("video",frame)
    key = cv.waitKey(1)
    if(key == ord('a')):
        break


cap.release()    
cv.destroyAllWindows()

client.loop_stop()