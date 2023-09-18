#//to create webcam
import cv2 #//opencv-module
import pickle
import numpy as np
import os
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
face_data=[]
#here we created an empty list
i=0 #initialize
name=input("Enter Your Name:") # take the name from user
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
        resized_image = cv2.resize(crop_image,(50,50))
        #(50,50) is the size to which image should be resized
        # we will store the resized image into the list
        #we are going to take the images after 10 frames
        if len(face_data)<=100 and i%10==0:
            face_data.append(resized_image)
        i=i+1
        #to see how many images have been takes
        cv2.putText(frame,str(len(face_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),1)
        #FONT_HERSHEY is the font
        #1 is font scale
        #and last one is color
        # and 1 is thickness
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),1)
        #now we are going to crop the images and store them in a list called faces and 
        # a name will be associated with it and we will also resize it 15x50
        
        
    #//now we will show the frame
    cv2.imshow("frame",frame)
    #//to add the keyword binding function
    k=cv2.waitKey(1) #//1 for infinite time
    if k==ord('q') or len(face_data)==100: #//when passed q from the keyboard
        break #//infinite loop and video frame will be gone
    
#//we will release the stored video
video.release()
#//now we will destroy all the windows
cv2.destroyAllWindows()

#to convert face data into numpy array
face_data = np.asarray(face_data)
#reshape data so that we acn use it into ML model
#as we are taking 100 images so the vector size should be 100
face_data=face_data.reshape(100,-1)
#now we will store the data into pickle file so that we can store it later

#check if file is present
#if it is available then we will just overwrite
#or else we will create a new file

if 'name.pkl' not in os.listdir('data/'):
    #we will create new file
    names = [name]*100 #list
    with open('data/name.pkl','wb') as f:
        #we will save it into our pickle file
        pickle.dump(names,f) #this will take 2 parameters
        #1. object
        #2. file , we have file but we dont have object
else: #if file is available
    with open('data/name.pkl','rb') as f: #rb-read mode
        #we will save it into our pickle file
        names=pickle.load(f) #this will take 2 parameters
    names = names + {name}*100
    #now we need to dump it inside our data folder
    with open('data/name.pkl','wb') as f:
        #we will save it into our pickle file
        pickle.dump(names,f) #this will take 2 parameters

#we will do the same thing as above for the face_data.pkl file
if 'face_data.pkl' not in os.listdir('data/'):
    #we will create new file
    with open('data/face_data.pkl','wb') as f:
        #we will save it into our pickle file
        pickle.dump(face_data,f) #this will take 2 parameters
        #1. object
        #2. file , we have file but we dont have object
else: #if file is available
    with open('data/face_data.pkl','rb') as f:
        #we will save it into our pickle file
        faces_data=pickle.load(f) #this will take 2 parameters
    faces_data = np.append(faces_data,face_data,axis=0)
    #now we need to dump it inside our data folder
    with open('data/face_data.pkl','wb') as f:
        #we will save it into our pickle file
        pickle.dump(faces_data,f) #this will take 2 parameters