#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install opencv-contrib-python')
get_ipython().system('pip install mediapipe opencv-python')


# In[1]:


import cv2
import mediapipe as mp
import numpy as np
import winsound
mp_drawing = mp.solutions.drawing_utils #give us the drawing utalities(visulazation of poses)
mp_pose = mp.solutions.pose #importing pose estimation model 



def calculate_angle(a,b,c):
    a = np.array(a)
    b= np.array(b)
    c= np.array(c)
   
    
    radians= np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0]) #radients for perticular joints
    
    angle =np.abs(radians*180.0/np.pi)
    if angle>180.0:
        angle = 360-angle
    return angle 



# In[2]:


def right_laterial_raise():
                counter = 0
                frequency_a = 800
                frequency_b = 400
                duration = 200

                cap = cv2.VideoCapture(0)


                with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:#.Pose is accessing "pose estimation" model, we can inc or dec the arf value depending on the requirement of accurecy 
                    while cap.isOpened(): 
                     ret,frame = cap.read() #frame will give us the image from webcam
                       # Recoloring the image to RGB
                     image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #recoloring the frame(feed from webcam) BGR to RGB 
                     image.flags.writeable = False #performance tuning ny setting wether or not our image iswriteable to fasle is basically going to saving bunch of memeory once we pass it to our pose estimation model 

                        # make detection 
                     result = pose.process(image) #accesing the pose model, .process(by processing it we're goinh to get our detection backand then we store those detection in result)

                        # Recolor back to BGR
                     image.flags.writeable = True 
                     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                     #Extract Landmar
                     try:
                        landmarks = result.pose_landmarks.landmark

                        #get co-ordinates
                        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]



                        #generate angle
                        right_angle_1= calculate_angle(right_shoulder,right_elbow,right_wrist)
                        right_angle_2 = calculate_angle(right_hip,right_shoulder,right_elbow)

                        right_int_angle_1 = int(right_angle_1)
                        right_int_angle_2 = int(right_angle_2)

                        #visualize angle

                        cv2.putText(image,str(right_int_angle_1),
                                            tuple(np.multiply(right_elbow,[640,480]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2,cv2.LINE_AA
                                       )

                        cv2.putText(image,str(right_int_angle_2),
                                            tuple(np.multiply(right_shoulder,[640,480]).astype(int)),
                                            cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2,cv2.LINE_AA
                                       ) 


                        #laterial raise logic
                        if right_int_angle_1 <180 and right_int_angle_1>140 and right_int_angle_2<100 and right_int_angle_2>=80 and stance =="Down":
                            counter +=1
                            winsound.Beep(frequency_a,duration)
                            stance = "up"
                            case = True
                        if right_int_angle_2>100 and stance == "up":
                            counter-=1
                            winsound.Beep(frequency_b,duration)
                            stance = None
                            case = False
                        if right_int_angle_2>20 and right_int_angle_2<70:
                            case = False
                        if right_int_angle_2<20 :
                            stance = "Down"
                            case = False

                     except:
                        pass


                     
                     #setup box
                     cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
                     cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)
                    
                     #Repetation Data 
                        
                     cv2.putText(image,'REPS',(15,20),
                                     cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1,cv2.LINE_AA)
                     cv2.putText(image,'Lateral Raise',(450,25),
                                     cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
                     cv2.putText(image,str(counter),(10,70),
                                     cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)
                        
                     #Render detections
                     if case == True:
                         mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                              mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                                     )


                     elif case == False:    
                         mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,## Drawing our detection, we pass our image, .pose_landmarks(it will give us all the land marks, .pose_connection (show the connection to betw landmark)
                                              mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                              mp_drawing.DrawingSpec(color = (0,0,225),thickness = 2, circle_radius = 5)
                                               ) 





                     cv2.imshow('Mediapipe Feed',image) #cv2.imshow gives us a pop on the screen that allows us to visulaise a perticular image #wechange frame to image
                     if cv2.waitKey(10) & 0xFF == ord('q'):
                        break#wethere or not we close our screen(0xFF checks what key we hit on our key board 'q' in our case)

                    cap.release() #release the webcamqqq
                    cv2.destroyAllWindows() #close the videofeed


# In[3]:


def left_laterial_raise():

            cap = cv2.VideoCapture(0)
            counter = 0
            frequency_a = 800
            frequency_b = 400
            duration = 200
            

            with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:#.Pose is accessing "pose estimation" model, we can inc or dec the arf value depending on the requirement of accurecy 
                while cap.isOpened(): 
                 ret,frame = cap.read() #frame will give us the image from webcam
                   # Recoloring the image to RGB
                 image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #recoloring the frame(feed from webcam) BGR to RGB 
                 image.flags.writeable = False #performance tuning ny setting wether or not our image iswriteable to fasle is basically going to saving bunch of memeory once we pass it to our pose estimation model 

                    # make detection 
                 result = pose.process(image) #accesing the pose model, .process(by processing it we're goinh to get our detection backand then we store those detection in result)

                    # Recolor back to BGR
                 image.flags.writeable = True 
                 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                 #Extract Landmar
                 try:
                    landmarks = result.pose_landmarks.landmark

                    #get co-ordinates

                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]



                    #generate angle

                    left_angle_1= calculate_angle(left_shoulder,left_elbow,left_wrist)
                    left_angle_2 = calculate_angle(left_hip,left_shoulder,left_elbow)

                    left_int_angle_1 = int(left_angle_1)
                    left_int_angle_2 = int(left_angle_2)
                    #visualize angle

                    cv2.putText(image,str(left_int_angle_1),
                                tuple(np.multiply(left_elbow,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2,cv2.LINE_AA
                               )

                    cv2.putText(image,str(left_int_angle_2),
                                tuple(np.multiply(left_shoulder,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2,cv2.LINE_AA
                               )


                   #laterial raise logic
                    if left_int_angle_1 <180 and left_int_angle_1>140 and left_int_angle_2<100 and left_int_angle_2>=80 and stance == "Down":
                        counter +=1
                        
                        
                        stance = "up"
                        case = True
                        winsound.Beep(frequency_a,duration)
                    if left_int_angle_2>100 and stance == "up":
                        counter-=1
                        stance = None
                        case = False
                        winsound.Beep(frequency_b,duration)
                    if left_int_angle_2>20 and left_int_angle_2<70:
                        case = False
                    if left_int_angle_2<20:
                        stance = "Down"
                        case = False

                 except:
                    pass


                  
                 #setup box
                 cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
                 cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)

                 #Repetation Data 
                 cv2.putText(image,'REPS',(15,20),
                                 cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,'Lateral Raise',(450,25),
                                 cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,str(counter),(10,70),
                                 cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)
                
                 #Render detections   
                 if case == True:
                     mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                                 )

                 elif case == False:    
                     mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,## Drawing our detection, we pass our image, .pose_landmarks(it will give us all the land marks, .pose_connection (show the connection to betw landmark)
                                          mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (0,0,225),thickness = 2, circle_radius = 5)
                                           ) 





                 cv2.imshow('Mediapipe Feed',image) #cv2.imshow gives us a pop on the screen that allows us to visulaise a perticular image #wechange frame to image
                 if cv2.waitKey(10) & 0xFF == ord('q'):
                    break#wethere or not we close our screen(0xFF checks what key we hit on our key board 'q' in our case)

                cap.release() #release the webcamqqq
                cv2.destroyAllWindows() #close the videofeed




# In[4]:


def hamstring_RDL():
        cap = cv2.VideoCapture(0)
        counter = 0
        stage = None
        case = None
        frequency  = 800
        duration = 200
        with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
            while cap.isOpened(): 
             ret,frame = cap.read() 
               # Recoloring the image to RGB
             image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
             image.flags.writeable = False 

                # make detection 
             result = pose.process(image) 

                # Recolor back to BGR
             image.flags.writeable = True 
             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

             #Extract Landmarks
             try:
                landmarks = result.pose_landmarks.landmark
                #get co-ordinates
                shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]



                #generate angle
                angle_1_right= calculate_angle(shoulder_right,hip_right,knee_right)
                angle_2_right = calculate_angle(hip_right,knee_right,ankle_right)

                int_angle_1_right = int(angle_1_right)
                int_angle_2_right = int(angle_2_right)


                #visualize angle
                cv2.putText(image,str(int_angle_1_right),
                                tuple(np.multiply(hip_right,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                           )

                cv2.putText(image,str(int_angle_2_right),
                                tuple(np.multiply(knee_right,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                           )
                
                #Hamstring_RDL logic
                if int_angle_1_right >160 and int_angle_2_right >160 :
                        stance = "up"
                        case = False

                if int_angle_1_right <=80 and int_angle_2_right >130 and int_angle_2_right<160 and stance =="up" :
                        stance = "Down"
                        counter +=1
                        print(counter)
                        case = True
                        winsound.Beep(frequency,duration)

             except:
                pass
              #setup repetation box
             cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
             cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)
            

             #Repetation Data 
             cv2.putText(image,'REPS',(15,12),
                         cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
             cv2.putText(image,'RDL',(450,25),
                         cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
             cv2.putText(image,str(counter),(10,60),
                         cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)

             #Render detections
             if case == True:

                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color = (0,44,0),thickness = 2, circle_radius = 5),
                                      mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                       )  
             elif case == False:

                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color = (245,117,66),thickness = 2, circle_radius = 5),
                                      mp_drawing.DrawingSpec(color = (245,66,230),thickness = 2, circle_radius = 5)
                                       )                  






             cv2.imshow('Mediapipe Feed',image) 
             if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            cap.release() 
            cv2.destroyAllWindows() 


# In[5]:


def right_bicep_curl():
        counter = 0
        stance = None
        frequency_a = 800
        duration = 200
        case = None
        cap = cv2.VideoCapture(0)

        with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
            while cap.isOpened(): 
             ret,frame = cap.read()
             image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
             image.flags.writeable = False 

             # make detection 
             result = pose.process(image) 
            # Recolor back to BGR
             image.flags.writeable = True 
             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

             #Extract Landmar
             try:
                landmarks = result.pose_landmarks.landmark

                #get co-ordinates
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]



                #generate angle
                right_angle_1= calculate_angle(right_shoulder,right_elbow,right_wrist)
                right_angle_2 = calculate_angle(right_elbow,right_shoulder,right_hip)
                right_int_angle_1 = int(right_angle_1)
                right_int_angle_2 = int(right_angle_2)
                #visualize angle
                cv2.putText(image,str(right_int_angle_1),
                                tuple(np.multiply(right_elbow,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2,cv2.LINE_AA
                           )

                cv2.putText(image,str(right_int_angle_2),
                                tuple(np.multiply(right_shoulder,[640,480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2,cv2.LINE_AA
                           )

                #curl logic 

                if  right_int_angle_1 >150 and  right_int_angle_2>0 and  right_int_angle_2<10 :
                    stance = "Down"
                    case = False


                if  right_int_angle_1 <60 and  right_int_angle_2>0 and  right_int_angle_2<10 and stance == "Down":

                    stance = "up"
                    counter +=1
                    case = True
                    winsound.Beep(frequency_a,duration)
                if  right_int_angle_1>60 and  right_int_angle_1<150 and  right_int_angle_2>0 and  right_int_angle_2<10:
                    case = False




             except:
                pass
             #render curl counter 

             cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
             cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)
             #Repetation Data 
             cv2.putText(image,'REPS',(15,20),
                         cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1,cv2.LINE_AA)
             cv2.putText(image,'Bicep Curls',(450,25),
                         cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
             cv2.putText(image,str(counter),(10,70),
                         cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)
             #setup box

             #Render detections
             if case == True:
                 mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                      mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                             )

             elif case == False:    


                 mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,## Drawing our detection, we pass our image, .pose_landmarks(it will give us all the land marks, .pose_connection (show the connection to betw landmark)
                                      mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                      mp_drawing.DrawingSpec(color = (0,0,225),thickness = 2, circle_radius = 5)
                                       ) 





             cv2.imshow('Mediapipe Feed',image) #cv2.imshow gives us a pop on the screen that allows us to visulaise a perticular image #wechange frame to image
             if cv2.waitKey(10) & 0xFF == ord('q'):
                break#wethere or not we close our screen(0xFF checks what key we hit on our key board 'q' in our case)

            cap.release() #release the webcamqqq
            cv2.destroyAllWindows() #close the videofeed


# In[6]:


def left_bicep_curl():
            counter = 0
            stance = None
            frequency_a = 800
            duration = 200
            case = None
            cap = cv2.VideoCapture(0)

            with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
                while cap.isOpened(): 
                 ret,frame = cap.read()
                 image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
                 image.flags.writeable = False 

                 # make detection 
                 result = pose.process(image) 
                # Recolor back to BGR
                 image.flags.writeable = True 
                 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                 #Extract Landmar
                 try:
                    landmarks = result.pose_landmarks.landmark

                    #get co-ordinates
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]



                    #generate angle
                    left_angle_1= calculate_angle(left_shoulder,left_elbow,left_wrist)
                    left_angle_2 = calculate_angle(left_elbow,left_shoulder,left_hip)
                    left_int_angle_1 = int(left_angle_1)
                    left_int_angle_2 = int(left_angle_2)
                    #visualize angle
                    cv2.putText(image,str(left_int_angle_1),
                                    tuple(np.multiply(left_elbow,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2,cv2.LINE_AA
                               )

                    cv2.putText(image,str(left_int_angle_2),
                                    tuple(np.multiply(left_shoulder,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2,cv2.LINE_AA
                               )

                    #curl logic

                    if  left_int_angle_1 >150 and  left_int_angle_2>0 and  left_int_angle_2<10 :
                        stance = "Down"
                        case = False


                    if  left_int_angle_1 <60 and  left_int_angle_2>0 and  left_int_angle_2<10 and stance == "Down":

                        stance = "up"
                        counter +=1
                        case = True
                        winsound.Beep(frequency_a,duration)
                    if  left_int_angle_1>60 and  left_int_angle_1<150 and  left_int_angle_2>0 and  left_int_angle_2<10:
                        case = False




                 except:
                    pass
                 #render curl counter 

                 cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
                 cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)
                 #Repetation Data 
                 cv2.putText(image,'REPS',(15,20),
                             cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,'Bicep Curls',(450,25),
                             cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,str(counter),(10,70),
                             cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)
                 #setup box

                 #Render detections
                 if case == True:
                     mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                                 )

                 elif case == False:    


                     mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,## Drawing our detection, we pass our image, .pose_landmarks(it will give us all the land marks, .pose_connection (show the connection to betw landmark)
                                          mp_drawing.DrawingSpec(color = (0,0,0),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (0,0,225),thickness = 2, circle_radius = 5)
                                           ) 





                 cv2.imshow('Mediapipe Feed',image) #cv2.imshow gives us a pop on the screen that allows us to visulaise a perticular image #wechange frame to image
                 if cv2.waitKey(10) & 0xFF == ord('q'):
                    break#wethere or not we close our screen(0xFF checks what key we hit on our key board 'q' in our case)

                cap.release() #release the webcamqqq
                cv2.destroyAllWindows() #close the videofeed


# In[7]:


def squats():
            cap = cv2.VideoCapture(0)

            #squat counter
            counter = 0
            stage = None 
            case = None
            frequency  =1000
            duration = 400 #ms
            #setup mediapipe instance 
            with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
                while cap.isOpened(): 
                 ret,frame = cap.read() 
                   # Recoloring the image to RGB
                 image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 
                 image.flags.writeable = False 

                    # make detection 
                 result = pose.process(image) 

                    # Recolor back to BGR
                 image.flags.writeable = True 
                 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                 #Extract Landmarks

                 try:
                    landmarks = result.pose_landmarks.landmark

                    #get co-ordinates
                    shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]


                    #generate angle
                    angle_1_right= calculate_angle(shoulder_right,hip_right,knee_right)
                    angle_2_right = calculate_angle(hip_right,knee_right,ankle_right)

                    angle_1_left= calculate_angle(shoulder_left,hip_left,knee_left)
                    angle_2_left = calculate_angle(hip_left,knee_left,ankle_left)

                    int_angle_1_right = int(angle_1_right)
                    int_angle_2_right = int(angle_2_right)

                    int_angle_1_left = int(angle_1_left)
                    int_angle_2_left = int(angle_2_left)
                    #visualize angle
                    cv2.putText(image,str(int_angle_1_right),
                                    tuple(np.multiply(hip_right,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                               )

                    cv2.putText(image,str(int_angle_2_right),
                                    tuple(np.multiply(knee_right,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                               )
                    cv2.putText(image,str(int_angle_1_left),
                                    tuple(np.multiply(hip_left,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                               )

                    cv2.putText(image,str(int_angle_2_left),
                                    tuple(np.multiply(knee_left,[640,480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2,cv2.LINE_AA
                               ) 

                    #squats logic                   
  
                    if int_angle_1_right <=65 and int_angle_2_right<= 65 and int_angle_1_left <=65 and int_angle_2_left <= 65:
                            stance = "Down"
                            case = True
                    if int_angle_2_right >90 and int_angle_2_left >90 and stance =="Down":
                            stance = "up"
                            counter +=1
                            winsound.Beep(frequency,duration)
                            print(counter)
                            case = False




                 except:
                    pass

                 #setup repetation box
                 cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
                 cv2.rectangle(image,(450,0),(650,50),(245,117,16),-1)

                 #Repetation Data 
                 cv2.putText(image,'REPS',(15,12),
                             cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,'Squats',(450,25),
                             cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),1,cv2.LINE_AA)
                 cv2.putText(image,str(counter),(10,60),
                             cv2.FONT_HERSHEY_SIMPLEX,2,(225,225,225),2,cv2.LINE_AA)

                 #Render detections
                 if case == True:   
                         mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color = (0,44,0),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (0,225,0),thickness = 2, circle_radius = 5)
                                           )

                 elif case == False:      
                         mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,## Drawing our detection, we pass our image, .pose_landmarks(it will give us all the land marks, .pose_connection (show the connection to betw landmark)
                                          mp_drawing.DrawingSpec(color = (245,117,66),thickness = 2, circle_radius = 5),
                                          mp_drawing.DrawingSpec(color = (245,66,230),thickness = 2, circle_radius = 5)
                                           )                  




                 cv2.imshow('Mediapipe Feed',image) 
                 if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

                cap.release() 
                cv2.destroyAllWindows() 


# In[8]:


print('List of exercise: right laterial raise , left laterial raise, hamstring RDL, right bicep curl, left bicep curl, squat')

input_data = input('Enter the exercise(as per the list):')

if input_data == 'right laterial raise':
    right_laterial_raise()
elif input_data == 'left laterial raise':
    left_laterial_raise()
elif input_data == 'hamstring RDL':
    hamstring_RDL()
elif input_data == 'right bicep curl':
    right_bicep_curl()
elif input_data == 'left bicep curl':
    left_bicep_curl()
elif input_data == 'squat':
    squat()


# In[ ]:




