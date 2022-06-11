# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 21:20:56 2022

@author: Evaldas
"""

import cv2
import mediapipe as mp
import numpy as np


import os.path
import csv

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

lWristArray = []

#vaizdo transliavimas
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        #keitimas į RGB
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        #aptikimas
        results = pose.process(image)
        
        #keitimas į BGR
        image.flags.writeable = True 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #žymių saugojimas
        try:
            landmarks = results.pose_landmarks.landmark
            #print(landmarks)
            for lndmrk in mp_pose.PoseLandmark:
                print(lndmrk)
            #print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
            lWrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z
                      ]
            lWristArray.append([lWrist[0]*5, lWrist[1]*(-5), lWrist[2]*5])
        except:
            pass  
        

        
        #atvaizdavimas
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(240,117,60), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(240,70,220), thickness=2, circle_radius=2),
                                  )
        
        cv2.imshow('Mediapipe Feed', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
#header = ['Name', 'M1 Score', 'M2 Score']
#data = [['Alex', 62, 80], ['Brad', 45, 56], ['Joey', 85, 98]]
data = lWristArray


dataFileID = '0'

while os.path.exists('samples/lWristPoints_' + dataFileID + '.csv'):
    dataFileID = str(int(dataFileID)+1)
    

filename = 'samples/lWristPoints_' + dataFileID + '.csv'
with open(filename, 'w') as file:
    
    for row in data:
        for x in row:
            file.write(str(x)+', ')
        file.write('\n')
        
    #f= open("samples/test1.txt","w+")
    #for i in range(len(lWristArray)):
     #f.write(str(5*lWristArray[i][0]) + ', ' + str(-5*lWristArray[i][1]) + ', ' + str(5*lWristArray[i][2]))
     #f.write('\n')
     #
    #f.close()
    
    
