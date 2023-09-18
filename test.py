# sourcery skip: hoist-statement-from-if, use-fstring-for-concatenation
from sklearn.neighbors import KNeighborsClassifier
#//to create webcam
import cv2 #//opencv-module
import pickle
import numpy as np
import os
#to add the attendance, we need to
import csv
#we are going to save the attendance in 2 columns
#1. name
#2.time
import keyboard
import time
#we need to store the time
from datetime import datetime
# to store the attendance according to date
#make sound when attendance is taken
from win32com.client import Dispatch

def speak(strl):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(strl)

#//to capture frame
video = cv2.VideoCapture(0)  #//0 means that we are using webcam of laptop and 1 for the external webcam
#//we are storing the captured frame in a variable
#//to detect the face
faceDetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
#to detect the face we need to convert the frame into grayscale as
# this cascade classifier is working well on periodical images 
# so we will convert them to bgr2 to grayscale
#as opencv reads the image in the bgr format
#we will create a list to store the face images and name associated with it
#we are loading the face_data and name from our data directory
with open('data/name.pkl','rb') as f: #rb-read mode
        #we will save it into our pickle file
    LABELS=pickle.load(f) #this will take 2 parameters
        
with open('data/face_data.pkl','rb') as f:
        #we will save it into our pickle file
    FACES=pickle.load(f) #this will take 2 parameters
        
#create an object for classification
knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABELS) # we need to fit our knn model according to the data

COL_NAMES=['NAME','TIME']



while True:
    ret,frame = video.read()  #//we are reading the frame using the read method
    #// the read method gives us 2 values 
    #//1. boolean value - if the webcam is okay or not
    #//2. frame
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #now we will detect the face
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    #1.3 and 5 are threshold values
    #now we are trying to get the coordinate values from the faces
    # that is x,y,w,h
    #x and y are coordinates w is width and h is height of the images
    # we will iterate through all the values here
    for (x,y,w,h) in faces:
        #now we will create a rectangle so that we can see that our face is detected
        # we will pass the original frame so that we dont need to see the grayscale frame at all
        # and we will pass the cardinal values that is x and y
        # width and height of the channel
        # color as red (50,50,255)
        # we will give thickness as 1
        #now we are going to crop the images and store them in a list called faces and 
        # a name will be associated with it and we will also resize it 15x50
        # in frame we will go from x to x+w
        # and y to y+h
        crop_image=frame[y:y+h,x:x+w,:]
        # now we will resize the images
        resized_image = cv2.resize(crop_image,(50,50)).flatten().reshape(1,-1)
        #(50,50) is the size to which image should be resized
        # we will store the resized image into the list
        #we are going to take the images after 10 frames
        #to see how many images have been takes
        output = knn.predict(resized_image)
        #storing time
        ts = time.time()
        #date instance
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        #time instance
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile("Attendance/Attendance_"+ date + ".csv")
        
        
        #to design the rectangle around the face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame,str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        #output[0] = name at first index of all the nearest 5 neighbors found out
        #origin/location
        #font
        #font scale
        #color
        #thickness
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)
        #now we are going to crop the images and store them in a list called faces and 
        # a name will be associated with it and we will also resize it 15x50
        #storing attendance in a list
        attendance = [str(output[0]),str(timestamp)]
        
    #//now we will show the frame
    cv2.imshow("frame",frame)
    #to pass attendance
    k=cv2.waitKey(1)
    if k & keyboard.is_pressed("o"):
        speak("Attendance taken..")
        time.sleep(5)
        if exist:
            with open("Attendance/Attendance_"+ date + ".csv","+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_"+ date + ".csv","+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    #//to add the keyword binding function
    
    if k & keyboard.is_pressed("q"): #//when passed q from the keyboard
        break #//infinite loop and video frame will be gone
    
#//we will release the stored video
video.release()
#//now we will destroy all the windows
cv2.destroyAllWindows()

#here, it finds the 5 nearest neighbors from the vector coming from the webcam
